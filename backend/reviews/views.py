from rest_framework import viewsets, permissions
# !!! ИМПОРТ 1: Для сортировки (Ordering)
from rest_framework.filters import OrderingFilter 
# !!! ИМПОРТ 2: Для фильтрации (DjangoFilterBackend)
from django_filters.rest_framework import DjangoFilterBackend 

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewReadSerializer

class ReviewsView(viewsets.ModelViewSet):
    
    #оптимизация запросов + фильтры
    queryset = Review.objects.all().select_related('game', 'user', 'platform')
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    

    filterset_fields = ['user', 'game', 'platform']
    

    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateSerializer
        return ReviewReadSerializer
    
    def perform_create(self, serializer): #при создании отзыва берется юзер его создававший
        serializer.save(
            user=self.request.user,
            is_critic=self.request.user.is_critic
        )