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


class Stuffs(models.Model):
    title = models.CharField(max_length=30)
    descriptinon = models.TextField()
    image = models.ImageField(upload_to='stuffs_image/', blank=True)
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


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Stuffs, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Stuffs, related_name='favorited_by', blank=True)
