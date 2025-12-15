from rest_framework import serializers
from django.utils import timezone
from .models import Game, Company, Genre, Platform

# Сериализаторы для моделей связанных с игрой
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description']
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        
class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name', 'description']

# Сериализатор для игр
class GameSerializer(serializers.ModelSerializer):
    
    # Вложенные сериализаторы для связей
    developer = CompanySerializer(read_only=True)
    publisher = CompanySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    
    # Поля для записи ID
    developer_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source='developer',
        write_only=True,
        help_text='ID разработчика'
    )
    
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source='publisher',
        write_only=True,
        help_text='ID издателя'
    )
    
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        source='genres',
        write_only=True,
        help_text='ID жанров'
    )
    
    platform_ids = serializers.PrimaryKeyRelatedField(
        queryset=Platform.objects.all(),
        many=True,
        source='platforms',
        write_only=True,
        help_text='ID платформ'
    )
    
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'title', 'description', 'developer', 'publisher', 
            'release_date', 'created_at', 'genres', 'platforms',
            'developer_id', 'publisher_id', 'genre_ids', 'platform_ids', 
            'review_count', 'average_rating'
        ]
        read_only_fields = ['id', 'created_at', 'review_count', 'average_rating']
        
    def get_review_count(self, obj):
        return obj.reviews.count() if hasattr(obj, 'reviews') else 0
    
    def get_average_rating(self, obj):
        return None
    
    # Валидация
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Название игры должно быть не менее 2 символов")
        if len(value) > 100:
            raise serializers.ValidationError("Название игры должно быть не более 100 символов")
        return value
    
    def validate(self, data):
        release_date = data.get('release_date')
        if release_date and release_date > timezone.now().date():
            raise serializers.ValidationError({
                'release_date': 'Дата релиза не может быть в будущем'
            })
        return data

#сериализатор для списка игр
class GameListSerializer(serializers.ModelSerializer):
    developer_name = serializers.CharField(source='developer.name', read_only=True)
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    genre_names = serializers.SerializerMethodField()
    platform_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'title', 'release_date', 
            'developer_name', 'publisher_name',
            'genre_names', 'platform_names'
        ]
        
    def get_genre_names(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    
    def get_platform_names(self, obj):
        return ", ".join([platform.name for platform in obj.platforms.all()])
    