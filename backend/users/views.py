from argparse import Action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from .serializers import RegistrationUserSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import generics, status, permissions, viewsets

User = get_user_model()

class RegistrationView(generics.CreateAPIView): #должен обрабатывать и делать регистрацию
    
    serializer_class = RegistrationUserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs): #переопределение родительского метода create - вызывается при нахождении DRF - класс RegistrationView
        serializer = self.get_serializer(data = request.data) #создаем сериализатор, он берет его из строчки serializer_class, где информация это информация из запроса
        serializer.is_valid(raise_exception=True) #проверка на валидацию - вызывает метод validate нашего сериализатора
        
        user = serializer.save() # вызывает еще один метод create
        
        refresh = RefreshToken.for_user(user) #создает токены для юзера
        
        
        access_token = str(refresh.access_token) #сохраняет токены для юзера
        refresh_token = str(refresh)
            
        return Response({           #посылает обратно ответ в виде Response - валидный тип ответа
            'user': UserSerializer(user).data, #преобразуем user в сериализатор, чтобы использовать data
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_201_CREATED)
        
        
    
    
class UserView(viewsets.ReadOnlyModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get', 'patch'], permission_classes = [permissions.IsAuthenticated]) 
    def me(self, request): #self.action = me - всегда, он находит этот url если мы введем .../me 
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data = request.data, partial = True)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)
        
        