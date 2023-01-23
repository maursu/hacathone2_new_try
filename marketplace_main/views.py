from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Cart, Category, Rating, Stuffs, Comments, CartItem, Cart
from rest_framework.decorators import api_view
from .serializers import CartSerializer, CategorySerializer, RatingSerializer, StuffsListSerializer, CommentsSerializer, StuffSerializer
from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permission import IsAdminAuthPermission, IsOwnerOrReadOnly

# Create your views here.


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StuffViewSet(ModelViewSet):
    queryset = Stuffs.objects.all()
    serializer_class = StuffSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'category']
    search_fields = ['created_at']
    ordering_fields = ['created_at', 'title']

    @action(['GET'], detail=True)
    def comments(self, request, pk=None): # Дополнительный маршрут для поста
        stuff = self.get_object()
        comments = stuff.comments.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    # @action(['POST', 'PATCH'], detail=True)
    # def rating(self,request, pk=None, **kwargs):
        
    #     if request.method == 'POST':
    #         data = request.data.copy()
    #         data['post'] = pk
    #         serializer = RatingSerializer(data=data,context = {'request':request})
    #         if serializer.is_valid(raise_exception=True) and not Rating.objects.filter(author=request.user, post=pk).exists():
    #             serializer.create(serializer.validated_data)
    #             return Response('рейтинг сохранен')
    #         else:
    #             return Response('Если вы хотите изменить оценку, сделайте это в разделе "изменения"')

    #     elif request.method == 'PATCH':
    #         data = request.data.copy()
    #         data['post'] = pk
    #         serializer = RatingSerializer(data = data,context = {'request':request})
    #         if serializer.is_valid(raise_exception=True) and Rating.objects.filter(author=request.user, post=pk).exists():
    #             instance = Rating.objects.get(author=request.user, post=pk)
    #             serializer.update(instance, request.data)
    #             return Response(f"Обновлен. Установлен рейтинг: {serializer.validated_data.get('rating')}")

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


#===========================================================
@api_view(['POST'])
def add_to_cart(request, slug):
    product = get_object_or_404(Stuffs, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['DELETE'])
def remove_from_cart(request, slug):
    product = get_object_or_404(Stuffs, slug=slug)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    serializer = CartSerializer(cart)
    return Response(serializer.data)