from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from games.models import Game, Cell

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ('id', 'row', 'column', 'mine', 'state', 'uncovered', 'value')

class GameSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'name', 'state', 'started', 'finished', 'rows', 'cols', 'mines', 'cells')
        read_only_fields = ('player', 'state', 'started', 'finished', 'cells')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
