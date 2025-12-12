from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



router = DefaultRouter()
router.register(r"reviews", views.ReviewsView, basename='reviews') #в views у нас идет выбор - создавать отзыв или просматривать его, все под url - reviews


urlpatterns = [
    path('', include(router.urls)),
]