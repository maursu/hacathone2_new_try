from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .views import StuffViewSet, FavoritesListView
from .models import Stuffs, Comments, Category, Favorites
from account.models import User
from django.core.files import File
from collections import OrderedDict
# Create your tests here.


class StuffsTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(title='cat1')
        user = User.objects.create_user(
            email ='test@gmail.com',
            password = '1234',
            is_active = True,
            name = 'test_name',
            last_name = 'test_last_name'
        )
        img = File(open('stuffs_image/2cc4f20786812d864cef0571e24c1cf6_4KM1clJ.jpg', 'rb'))
        stuffs = [
        Stuffs(seller=user, descriptinon = 'stuff', title='stuff1', image = img, category = self.category, slug=1, price = 100, quantity = 1),
        Stuffs(seller=user, descriptinon = 'stuff2', title='stuff2', image = img, category = self.category, slug=2, price = 100, quantity = 1),
        Stuffs(seller=user, descriptinon = 'stuff3', title='stuff3', image = img, category = self.category, slug=3, price = 100, quantity = 1)
        ]
        Stuffs.objects.bulk_create(stuffs)

    def test_list(self):
        request = self.factory.get('stuffs/')
        view = StuffViewSet.as_view({'get':'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        assert type(response.data) == OrderedDict

    def test_retrieve(self):
        slug = Stuffs.objects.all()[0].slug
        request = self.factory.get(f'stuffs/{slug}')
        view = StuffViewSet.as_view({'get':'retrieve'})
        response = view(request, pk=slug)
        assert response.status_code == 200

    # def test_create(self):
    #     user = User.objects.all()[0]
    #     print(user)
    #     print('==============================')
    #     data = {
    #         'description': 'Новый классный продукт, который не соответствует требованием никаких потребностей',
    #         'title': 'Чудо-нож',
    #         'category': 'cat1',
    #         'price':800,
    #         'quantity':1,
    #         'seller': user.email
    #     }
    #     request = self.factory.post('stuffs', data, format='json')
    #     force_authenticate(request, user=user)
    #     view = StuffViewSet.as_view({'stuffs':'create'})
    #     response = view(request)
    #     print(request)
    #     assert response.status_code == 201
    #     assert response.data['title'] == data['title']
    #     assert Stuffs.objects.filter(seller=user, body = data['title']).exists()

    def test_delete(self):
        user = User.objects.all()[0]
        print(user)
        slug = Stuffs.objects.all()[0].slug
        request = self.factory.delete(f'stuffs/{slug}')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view({'delete':'destroy'})
        response = view(request, pk=slug)
        assert response.status_code == 204

    def test_update(self):
        user = User.objects.all()[0]
        slug = Stuffs.objects.all()[0].slug
        data = {
            'description': 'Самая нужная вещь',
            'title': 'Балдежный сервилат',
            'price':1500,
            'quantity': 1500
        }
        request = self.factory.patch(f'stuffs/{slug}',data,format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view({'patch':'partial_update'})
        response = view(request, pk=slug)
        assert response.status_code == 200
    
    def test_comments(self):
        slug = Stuffs.objects.all()[0].slug
        request = self.factory.get(f'stuffs/{slug}/comments')
        view = StuffViewSet.as_view({'get':'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        assert type(response.data) == OrderedDict
    
    def test_patch_rating(self):
        user = User.objects.all()[0]
        slug = Stuffs.objects.all()[0].slug
        from random import randint
        data = {
            'rating': randint(1, 10)
        }
        request = self.factory.patch(f'stuffs/{slug}/rating/',data,format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view({'patch':'partial_update'})
        response = view(request, pk=slug)
        assert response.status_code == 200

    # def test_like(self):
    #     user = User.objects.all()[0]
    #     slug = Stuffs.objects.all()[0].slug
    #     request = self.factory.post(f'stuffs/{slug}/like/', format='json')
    #     force_authenticate(request, user=user)
    #     view = StuffViewSet.as_view({'post': 'create'})
    #     response = view(request)
    #     print(response.status_code)
    #     assert response.status_code == 201
        




# class FavoritesTest(APITestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         user = User.objects.create_user(
#             email ='test@gmail.com',
#             password = '1234',
#             is_active = True,
#             name = 'test_name',
#             last_name = 'test_last_name'
#         )
#         favorites = [
#         Favorites(user = user, product = 'product', favorite = True),
#         Favorites(user = user, product = 'product2', favorite = True),
#         ]
#         Favorites.objects.bulk_create(favorites)

    # def test_favorite(self):
    #     user = User.objects.all()[0]
    #     pk = Favorites.objects.all()
    #     print(pk)
    #     request = self.factory.delete(f'favorites/{pk}')
    #     force_authenticate(request, user=user)
    #     view = FavoritesListView.as_view({'delete':'destroy'})
    #     response = view(request, pk=pk)
    #     assert response.status_code == 204