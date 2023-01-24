from django.shortcuts import render
from rest_framework import generics
from .models import Category, Rating, Stuffs, Comments, Favorites 
from .serializers import CategorySerializer, RatingSerializer, StuffsListSerializer, CommentsSerializer, StuffSerializer, FavoritesSerializer
from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permission import IsAdminAuthPermission, IsOwnerOrReadOnly

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
    filterset_fields = ['title', 'category']
    search_fields = ['created_at']
    ordering_fields = ['created_at', 'title']

    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
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
    def favorite(self,request,pk):
        product = self.get_object()
        user = request.user
        try:
            favorites = Favorites.objects.get(product=product, user=user)
            favorites.favorites = not favorites.favorites
            favorites.save()
            message = 'Added to favorites' if favorites.favorites else 'Deleted from favorites'
            if not favorites.favorites:
                favorites.delete()
        except Favorites.DoesNotExist:
            Favorites.objects.create(product=product, user=user, favorites=True)
            message = 'favorite'
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
            self.permission_classes = [IsOwnerOrReadOnly]          
        
        return super().get_permissions() 


class FavoritesListView(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]
        elif self.action in ['update','partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]          
        
        return super().get_permissions()


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