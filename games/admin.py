from django.contrib import admin
from . models import Genre, Game, Company, Platform


admin.site.register(Genre)
admin.site.register(Company)
admin.site.register(Game)
admin.site.register(Platform)