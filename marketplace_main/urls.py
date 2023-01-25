from django.urls import path, include
from .views import CategoryListView, CommentCreateView, StuffViewSet,CommentCreateView, FavoritesListView, similar_products
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stuffs',StuffViewSet)
router.register('comments', CommentCreateView)
router.register('categories', CategoryListView)


urlpatterns = [
    path('similar/<str:slug>/', similar_products, name='similar_products'),
    path('', include(router.urls)),
    path('favorites/', FavoritesListView.as_view()),
    path('favorites/<int:pk>/', FavoritesListView.as_view())

]