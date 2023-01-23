from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

# Create your models here.
User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()
    
    # class Meta:
    #     verbose_name = 'Category'
    #     verbose_name_plural = "Categories"


class Stuffs(models.Model):
    title = models.CharField(max_length=30)
    descriptinon = models.TextField()
    image = models.ImageField()
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='stuffs')
    posted_at = models.DateField(auto_now_add=True)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()
    
    class Meta:
        verbose_name = 'Stuff'
        verbose_name_plural = "Stuffs"


# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
#     quantity = models.IntegerField()
#     title = models.ForeignKey(Stuffs, on_delete=models.CASCADE, related_name='cart')

#     def __str__(self) -> str:
#         return self.title


class Rating(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()
    stuff = models.ForeignKey(Stuffs, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self) -> str:
        return f'Stuff: {self.stuff} - Rating: {self.rating}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = "Rating"


class Comments(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='comments')
    stuff = models.ForeignKey(Stuffs, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.body
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = "Commentaries"


#_________________________________________________________________________________________

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total(self):
        total = 0
        for item in self.items.all():
            total += item.stuffs.price * item.quantity
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Stuffs, on_delete=models.CASCADE)
    quantity = models.IntegerField()