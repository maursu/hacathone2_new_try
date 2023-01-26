from rest_framework import serializers
from .models import Category, Comments, Rating, Stuffs, Favorites, Cart, Order
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('title',)


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    def create(self,validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comments.objects.create(author=user, **validated_data)
        return comment

    class Meta:
        model = Comments
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Favorites
        fields = ('user','product', 'favorites')
   

class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    
    class Meta:
        model = Rating
        fields = '__all__'

    def create(self,validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating

    def validate_rating(self, rating):
        if rating not in range(1,11):
            raise serializers.ValidationError('Необходимо указать рейтинг от 1 до 10 включительно!')
        return rating

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


class StuffsListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stuffs
        fields = '__all__'


class StuffSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stuffs
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentsSerializer(Comments.objects.filter(stuff=instance.pk), many=True).data
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['likes'] = instance.likes.count()
        representation['favorites'] = FavoritesSerializer(Favorites.objects.filter(favorites=True, product=instance.pk), many = True).data
        return representation


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'

    total_price = 0
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        self.total_price += instance.price
        return representation


    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'
