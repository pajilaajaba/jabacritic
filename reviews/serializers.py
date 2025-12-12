from rest_framework import serializers

from .models import Review
from games.serializers import GameSerializer, PlatformSerializer
from users.serializers import UserSerializer


#Сериализатор для чтения данные - запроса GET
class ReviewReadSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only = True)
    game = GameSerializer(read_only = True)
    platform = PlatformSerializer(read_only = True)
    
    
    class Meta:
        model = Review
        fields = '__all__'
        
#Сериализатор для добавления/обновления данныъ - PUT, POST
class ReviewCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = [
            'game', 'platform','description', 'rating'
        ]
        
    def validate_rating(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('Рейтинг от 0 до 100')
        return value