import random
import datetime
import pytz
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .cell import Cell

class Game(models.Model):
    STATE_NEW = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    STATE_WON = 3
    STATE_LOST = 4
    STATE_CHOICES = (
        (STATE_NEW, 'new'),
        (STATE_PLAYING, 'playing'),
        (STATE_PAUSED, 'paused'),
        (STATE_WON, 'won'),
        (STATE_LOST, 'lost'),
    )

    name = models.CharField(max_length=200, default='Game')
    player = models.ForeignKey(User, related_name='player', on_delete=models.CASCADE)

    state = models.IntegerField(choices=STATE_CHOICES, default=STATE_NEW)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)
    rows = models.IntegerField(default=8)
    cols = models.IntegerField(default=8)
    mines = models.IntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def game_action(self, row, col, action):
        cell = Cell.objects.get(game=self, row=row, column=col)

        if self.started == None:
            self.game_started()

        if action != 'flag' and cell.state == cell.FLAGGED:
            raise ValidationError('Cell is flagged, can\'t be modified. Unflag it first.')

        if action == 'flag':
            cell.set_flagged()
            if self.game_solved:
                self.game_won()
        elif action == 'question':
            cell.set_question()
        elif action == 'reveal':
            if cell.mine:
                cell.set_exploded()
                self.game_lost()
            else:
                self.uncover_cell(cell)
                if self.game_solved:
                    self.game_won()
        else:
            return False

        return True

    @property
    def game_solved(self):
        mines_and_flagged_cells = self.cells.filter(state=2, mine=True)
        covered_cells = self.cells.exclude(mine=True).filter(uncovered=False)

        return len(mines_and_flagged_cells) == self.mines and len(covered_cells) == 0

    def game_started(self):
        self.state = self.STATE_PLAYING
        self.started = timezone.now()
        self.save()

    def game_ended(self):
        self.finished = timezone.now()
        self.save()

    def game_won(self):
        self.state = self.STATE_WON
        self.game_ended()

    def game_lost(self):
        self.state = self.STATE_LOST
        self.game_ended()

    def uncover_cell(self, cell):
        if cell.state == cell.COVERED:
            cell.set_uncovered()
            if self._count_adjacent_with_mines(cell) == 0:
                for c in self._adjacent_cells(cell):
                    self.uncover_cell(c)

    def _adjacent_cells(self, cell):
        positions = [
            # up left
            {
                'row': cell.row - 1,
                'col': cell.column - 1
            },
            # up
            {
                'row': cell.row - 1,
                'col': cell.column
            },
            # up right
            {
                'row': cell.row - 1,
                'col': cell.column + 1
            },
            # right
            {
                'row': cell.row,
                'col': cell.column + 1
            },
            # down right
            {
                'row': cell.row + 1,
                'col': cell.column + 1
            },
            # down
            {
                'row': cell.row + 1,
                'col': cell.column
            },
            # left down
            {
                'row': cell.row + 1,
                'col': cell.column - 1
            },
            # left
            {
                'row': cell.row,
                'col': cell.column - 1
            }
        ]
        cells = []
        for pos in positions:
            if self._within_board(pos['row'], pos['col']):
                try:
                    cell = Cell.objects.get(game=self, row=pos['row'], column=pos['col'], uncovered=False)
                    cells.append(cell)
                except Cell.DoesNotExist as err:
                    pass
        return cells

    def _count_adjacent_with_mines(self, cell):
        return sum(1 for cell in self._adjacent_cells(cell) if cell.mine)

    def _within_board(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

@receiver(post_save, sender=Game)
def init_game(sender, instance, created, **kwargs):
    if not created:
        return

    cells = []
    for row in range(instance.rows):
        for col in range(instance.cols):
            cells.append(Cell.objects.create(game=instance, row=row, column=col))
    for mine in random.sample(cells, instance.mines):
        mine.mine = True
        mine.save()