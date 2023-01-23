from django.urls import path, include
from .views import CategoryListView, CommentCreateView, StuffViewSet,CommentCreateView,  FavoriteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stuffs',StuffViewSet)
router.register('comments', CommentCreateView)
router.register('categories', CategoryListView)
router.register('favorites', FavoriteViewSet)


urlpatterns = [
    path('', include(router.urls)),

]