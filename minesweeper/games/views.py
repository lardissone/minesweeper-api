from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from games.models import Game
from games.serializers import GameSerializer, UserSerializer
from games.permissions import IsOwnerOrReadOnly

class GameViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
        Views for Games model

        retrieve:
        Return given game

        list:
        Lists all games

        create:
        Creates a new Game

        update:
        Update a Game
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'put']

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)

    def get_serializer_context(self, *args, **kwargs):
        return { 'request': self.request }

    def post(self, request, *args, **kwargs):
        mines = request.data.get('mines')
        rows = request.data.get('rows')
        cols = request.data.get('cols')
        if mines >= rows + cols:
            raise ValidationError('Mines shouldn\'t be higher than Columns + Rows')
        return self.create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        game = self.get_object()
        if game.state == game.STATE_WON or game.state == game.STATE_LOST:
            raise ValidationError('Game finished')
        elif game.state == game.STATE_PAUSED:
            raise ValidationError('Game paused')

        action = request.data.get('action')
        row = request.data.get('row')
        col = request.data.get('col')
        if row is None or col is None or row > game.rows or col > game.cols:
            raise ValidationError('Invalid cell position')

        game.game_action(row, col, action)
        serializer = GameSerializer(game, context={'request': request}, many=False)
        return Response(serializer.data)

    def list(self, request):
        queryset = Game.objects.all()
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

