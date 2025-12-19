from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce

from .models import Game, Company, Genre, Platform
from .serializers import (
    GameSerializer, GameListSerializer,
    CompanySerializer, GenreSerializer, PlatformSerializer
)

from .filters import GameFilter  

class GameViewSet(viewsets.ModelViewSet):
    
    queryset = Game.objects.all() \
        .select_related('developer', 'publisher') \
        .prefetch_related('genres', 'platforms') \
        .annotate(
            # если Avg вернет None, Coalesce заменит его на 0.0
            average_rating=Coalesce(Avg('reviews__rating'), Value(0.0))
        )
    
    # Фильтрация поиск и сортировка
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GameFilter  # Используем кастомный фильтр
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'release_date', 'created_at', 'average_rating']
    ordering = ['-created_at']  # Сортировка по умолчанию
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Возвращаем либо сериализатор списка игр либо просто игры
    def get_serializer_class(self):
        if self.action == 'list':
            return GameListSerializer
        return GameSerializer
    
    # Проверяем, чтобы создать, удалить, обновиить или частично обновить могли только пользователи с полем AdminUser == True
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    
    # Похожие игры по жанрам
    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        game = self.get_object()
        similar_games = Game.objects.filter(
            genres__in=game.genres.all()
        ).exclude(id=game.id).distinct()[:5]
        
        serializer = GameListSerializer(similar_games, many=True)
        return Response(serializer.data)
    
    #для того чтобы поставить/убрать лайк
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        game = self.get_object()
        user = request.user
        
        if user in game.favorites.all():
            game.favorites.remove(user)
            return Response({'status': False})
        else:
            game.favorites.add(user)
            return Response({'status': True})
        
    #
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_games = Game.objects.count()
        latest_game = Game.objects.order_by('-release_date').first()
        oldest_game = Game.objects.order_by('release_date').first()
        return Response({
            'total_games': total_games,
            'latest_release': latest_game.release_date if latest_game else None,
            'oldest_release': oldest_game.release_date if oldest_game else None,
            'latest_game': latest_game.title if latest_game else None,
        })
    
# Для обработки связанных полей
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']

class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']