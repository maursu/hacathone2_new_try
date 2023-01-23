from django.urls import path, include
from .views import CategoryListView, CommentCreateView, StuffViewSet,CommentCreateView, add_to_cart, remove_from_cart
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stuffs',StuffViewSet)
router.register('comm', CommentCreateView)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('', include(router.urls)),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
]