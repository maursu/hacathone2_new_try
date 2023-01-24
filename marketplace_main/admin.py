from django.contrib import admin
from .models import Category, Stuffs, Rating, Comments
from django.db.models import Avg
# Register your models here.

admin.site.register(Category)
# admin.site.register(Stuffs)
# admin.site.register(Rating)
admin.site.register(Comments)
class RatingInline(admin.TabularInline):
    model = Rating

@admin.register(Stuffs)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_at', 'price', 'quantity')
    inlines = [RatingInline]
    search_fields = ['title', 'posted_at']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-posted_at']
    list_filter = ['category__title','posted_at', ]

    def get_rating(self, obj):
        result = obj.ratings.aggregate(Avg('rating'))
        return result['rating__avg']