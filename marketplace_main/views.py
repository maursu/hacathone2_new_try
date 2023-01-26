from .models import Category, Rating, Stuffs, Comments, Favorites, Likes
from .serializers import CategorySerializer, RatingSerializer, StuffsListSerializer, CommentsSerializer, StuffSerializer, FavoritesSerializer
from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework import filters
from rest_framework.decorators import action, APIView,api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permission import IsAdminAuthPermission, IsOwnerOrReadOnly, IsSellerOdAdmin
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class CategoryListView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == ['create', 'update','partial_update', 'destroy']:
            self.permission_classes = [IsAdminAuthPermission, IsOwnerOrReadOnly]         
        
        return super().get_permissions()


class StuffViewSet(ModelViewSet):
    queryset = Stuffs.objects.all()
    serializer_class = StuffSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'category__slug']    #Фильтрация
    search_fields = ['category__slug','title',]
    ordering_fields = ['posted_at', 'title', 'price']
    ordering = ['title']

    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        print(request)
        stuff = self.get_object()
        comments = stuff.comments.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'PATCH'], detail=True)
    def rating(self,request, pk=None, **kwargs):
        if request.method == 'POST':
            data = request.data.copy()
            data['stuff'] = pk
            serializer = RatingSerializer(data=data,context = {'request':request})
            if serializer.is_valid(raise_exception=True) and not Rating.objects.filter(author=request.user, stuff=pk).exists():
                serializer.create(serializer.validated_data)
                return Response('рейтинг сохранен')
            else:
                return Response('Если вы хотите изменить оценку, сделайте это в разделе "изменения"')

        elif request.method == 'PATCH':
            data = request.data.copy()
            data['stuff'] = pk
            serializer = RatingSerializer(data = data,context = {'request':request})
            if serializer.is_valid(raise_exception=True) and Rating.objects.filter(author=request.user, stuff=pk).exists():
                instance = Rating.objects.get(author=request.user, stuff=pk)
                serializer.update(instance, request.data)
                return Response(f"Обновлен. Установлен рейтинг: {serializer.validated_data.get('rating')}")

    @action(['POST'], detail=True)
    def like(self,request,pk):
        stuff = self.get_object()
        user = request.user
        try:
            like = Likes.objects.get(stuff=stuff, author=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'like' if like.is_liked else 'like removed'
            if not like.is_liked:
                like.delete()
        except Likes.DoesNotExist:
            Likes.objects.create(stuff=stuff, author=user, is_liked=True)
            message = 'like'
        return Response(message, status=200)

    @action(['POST'], detail=True)
    def favorite(self,request,pk):
        product = self.get_object()
        user = request.user
        try:
            favorite = Favorites.objects.get(product=product, user=user)
            favorite.favorites = not favorite.favorites
            favorite.save()
            message = 'added in favorites' if favorite.favorites else 'removed from favorites'
            if not favorite.favorites:
                favorite.delete()
        except Favorites.DoesNotExist:
            Favorites.objects.create(product=product, user=user, favorites=True)
            message = 'added to favorites'
        return Response(message, status=200)

    def get_serializer_class(self):
        if self.action == 'list':
            return StuffsListSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]
        elif self.action in ['update','partial_update', 'destroy']:
            self.permission_classes = [IsSellerOdAdmin]          
        
        return super().get_permissions() 


class FavoritesListView(APIView):

    permission_classes = [IsAdminAuthPermission]

    def get(self,request):
        queryset = Favorites.objects.filter(user=request.user)
        serializer = FavoritesSerializer(queryset, many=True)
        return Response(serializer.data,status=200)
    def delete(self, request, pk):
        try:
            favorite = Favorites.objects.get(id=pk)
            deleted = favorite.product
            favorite.delete()
            return Response(f'{deleted} was deleted')
        except Favorites.DoesNotExist:
            return Response('This favorite does not exists')
     

class CommentCreateView(ModelViewSet):

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]
        elif self.action in ['update','partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]          
        
        return super().get_permissions()


@api_view(['GET'])
def similar_products(request, slug):
    stuffs = Stuffs.objects.get(slug=slug)
    similar_products = Stuffs.objects.filter(category=stuffs.category).exclude(slug=slug)
    serializer = StuffsListSerializer(similar_products, many=True)
    return Response(serializer.data)