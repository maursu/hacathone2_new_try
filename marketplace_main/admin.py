from django.contrib import admin
from .models import Category, Stuffs, Rating, Comments

# Register your models here.

admin.site.register(Category)
admin.site.register(Stuffs)
admin.site.register(Rating)
admin.site.register(Comments)