import django_filters
from django.db.models import Q
from .models import Game, Genre, Platform, Company


class GameFilter(django_filters.FilterSet): #Наследуем от стандратноого Filter в котором уже мног чего встроено
    search = django_filters.CharFilter(method='filter_search') #позволяет искать по нескольким полям если указать это в url - является кастомным фильтром для него
    genres = django_filters.ModelMultipleChoiceFilter(                  #нужна доп функция ниже - filter_search
        field_name='genres', 
        queryset= Genre.objects.all(),
        conjoined=True
    )
    platforms = django_filters.ModelMultipleChoiceFilter( #фильтр для множественного выбора
        field_name='platforms', # поле для фильтрации
        queryset=Platform.objects.all(), # выбираем место откуда брать варианты для выбора
        conjoined=True # Доп условие - если TRUE то будут выводить только игры, у которых есть ВСЕ выбранные жанры
        #Если FALSE то выводится игры, у которых есть любой из жанров поиска
    )
    developer = django_filters.ModelChoiceFilter( #Фильтр для одиночного выбора
        field_name='developer',
        queryset=Company.objects.all()
    )
    publisher = django_filters.ModelChoiceFilter(
        field_name='publisher',
        queryset=Company.objects.all()
    )
    release_year = django_filters.NumberFilter( #фильтр для чисел
        field_name='release_date',
        lookup_expr='year'       #Извлекаем из даты только год
    )
    min_year = django_filters.NumberFilter(
        field_name='release_date__year',
        lookup_expr='gte' #БОЛЬШЕ ИЛИ РАВНО (GREATER THAN OR EQUAL)
    )
    max_year = django_filters.NumberFilter(
        field_name='release_date__year',
        lookup_expr='lte'#Меньше или равно (LOWER THAN OR EQUEAL)
    )
    
    class Meta:
        model = Game
        fields = []
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        )
    
    ordering = django_filters.OrderingFilter(
        choices=(
            ('-created_at', 'Новые'),
            ('created_at', 'Старые'),
            ('-release_date', 'Сначала новые релизы'),
            ('release_date', 'Сначала старые релизы'),
            ('title', 'А-Я'),
            ('-title', 'Я-А'),
            # ('-average_rating', 'Высокий рейтинг'),
            # ('review_count', 'Много отзывов'),
        ),
        field_labels={
            'created_at': 'Дата добавления',
            'release_date': 'Дата релиза',
            'title': 'Название',
        }
    )