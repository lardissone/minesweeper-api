from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

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

class Cell(models.Model):
    COVERED = 0
    QUESTION = 1
    FLAGGED = 2
    UNCOVERED = 3
    CELL_STATE = (
        (COVERED, 'hidden'),
        (QUESTION, 'question'),
        (FLAGGED, 'flagged'),
        (UNCOVERED, 'uncovered'),
    )

    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='cells')
    row = models.IntegerField()
    column = models.IntegerField()
    mine = models.BooleanField(default=False)
    state = models.IntegerField(choices=CELL_STATE, default=COVERED)