from rest_framework import serializers
from .models import Cart, Category, Comments, Rating, Stuffs
from django.db.models import Avg


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('title',)


class CommentsSerializer(serializers.ModelSerializer):

    def create(self,validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comments.objects.create(author=user, **validated_data)
        return comment

    class Meta:
        model = Comments
        field = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating
        field = '__all__'
    
    def create(self,validated_data):
        request = self.context.get('request')
        user = request.user
        rating = Rating.objects.create(author=user, **validated_data)
        return rating

    def validate_rating(self, rating):
        if rating not in range(1,6):
            raise serializers.ValidationError('Необходимо указать рейтинг от 1 до 5 включительно!')
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
        return representation

#============================================

class CartSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)
    class Meta:
        model = Cart
        fields = '__all__'