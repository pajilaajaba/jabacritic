from email.mime import base
from django.urls import path, include
from .views import RegistrationView, UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserView, basename = 'users')

urlpatterns = [
    
    path('', include(router.urls)),
    
    path('register/', RegistrationView.as_view(), name = 'register'),
    path('login/', TokenObtainPairView.as_view(), name = 'login'),
    path('refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
]
