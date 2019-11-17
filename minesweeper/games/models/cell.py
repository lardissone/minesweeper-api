import random
from django.conf import settings
from django.db import models

class Cell(models.Model):
    COVERED = 0
    QUESTION = 1
    FLAGGED = 2
    EXPLODED = 3
    CELL_STATE = (
        (COVERED, 'hidden'),
        (QUESTION, 'question'),
        (FLAGGED, 'flagged'),
        (EXPLODED, 'exploded'),
    )

    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='cells')
    row = models.IntegerField()
    column = models.IntegerField()
    mine = models.BooleanField(default=False)
    state = models.IntegerField(choices=CELL_STATE, default=COVERED)
    uncovered = models.BooleanField(default=False)

    def __repr__(self):
        return 'Cell {},{}'.format(self.row, self.column)

    def set_flagged(self):
        self.state = self.FLAGGED if self.state != self.FLAGGED else self.COVERED
        self.uncovered = True
        self.save()

    def set_question(self):
        self.state = self.QUESTION if self.state != self.QUESTION else self.COVERED
        self.uncovered = True
        self.save()

    def set_uncovered(self):
        self.uncovered = True
        self.save()

    def set_exploded(self):
        self.state = self.EXPLODED
        self.uncovered = True
        self.save()
