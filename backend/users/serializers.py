from wsgiref import validate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from games.serializers import GameListSerializer


User = get_user_model()


#сериализатор для чтения, отображения пользователя - НЕ ДЛЯ СОЗДАНИЯ
class UserSerializer(serializers.ModelSerializer):
    favorite_games = GameListSerializer(many=True, read_only=True)
    # 1. Меняем на MethodField
    user_reviews = serializers.SerializerMethodField() 
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email' , 'is_critic', 
            'description', 'avatar', 'date_joined',
            'favorite_games', 'user_reviews'
        ]
        read_only_fields = ['id', 'date_joined']
        
    def get_user_reviews(self, obj):
        from reviews.serializers import SimpleReviewSerializer
        
        reviews = obj.reviews.all()
        
        return SimpleReviewSerializer(reviews, many=True).data
        
        
        
        
class RegistrationUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only = True, #только для записи не возвращается в ответе API
        style={'input_type': 'password'} #чтобы на фронтенде скрывался ввод пароля
    )
    password2 = serializers.CharField( #Второй пароль для сравнения с первым
        write_only = True,
        style={'input_type': 'password'}
    )
    
    
    class Meta:
        model = User
        fields =[
            'username', 'email' , 'is_critic', 
            'password1', 'password2', 
            'description', 'avatar',
        ]
        
    
    def validate(self, data): #когда DRF вызывает validate он передает туда наши указанные данные
        if data['password1'] != data['password2']: #проверка что два пароля совпадают 
            raise serializers.ValidationError('Пароли не совпадают')
        return data
    
    def create(self, validated_data): # когда DRF вызывает метод create
        validated_data.pop('password2')
        
        validated_data['password'] = validated_data.pop('password1') #меняем пароль1 на пароль, чтобы Django удобнее взаимодействовало
        user = User.objects.create_user(**validated_data)   #Возвращаем объект созданного ползователя по модели User, где данные у него =  распакованная словарь validated_data
        #create_user - автоматически хэширует пароль
        return user