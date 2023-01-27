from django.urls import path, include
from .views import CategoryListView, CommentCreateView, StuffViewSet,CommentCreateView, FavoritesListView, similar_products,CartView
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register('stuffs',StuffViewSet)
router.register('comments', CommentCreateView)
router.register('categories', CategoryListView),
router.register('cart', CartView)


urlpatterns = [
    path('similar/<str:slug>/', similar_products, name='similar_products'),
    path('', include(router.urls)),
    path('favorites/', FavoritesListView.as_view()),
    path('favorites/<int:pk>/', FavoritesListView.as_view())

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)