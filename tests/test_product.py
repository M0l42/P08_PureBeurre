from django.test import TestCase
from django.urls import reverse
from purebeurre.models import Product, Category, Favorite
from tests import create_testing_user


class ProductPageTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="test")
        self.product = Product.objects.get(name="test")

    def test_product_page_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('product', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_product_page_return_404(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse('product', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


class ProductSearchPageTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="test")
        self.product = Product.objects.get(name="test")

    def test_search_product_page_no_object(self):
        query = "zdqilhs"
        response = self.client.get(reverse('product_search'), {'query': query})
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_search_product_page_with_object(self):
        query = "est"
        response = self.client.get(reverse('product_search'), {'query': query})
        self.assertQuerysetEqual(response.context['object_list'], ['<Product: test>'])


class SubstitutePageTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="test category")
        self.product = Product.objects.create(name="test", category=category, nutrition_grade=None)
        self.product_without_category = Product.objects.create(name="test w/o category", nutrition_grade=None)
        self.substitute = Product.objects.create(name="test sub", category=category, nutrition_grade="a")
        create_testing_user()

    def test_search_substitute_page_no_object(self):
        product_id = self.product_without_category.id
        response = self.client.get(reverse('find_substitute', args=(product_id,)))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_search_substitute_page_with_object(self):
        product_id = self.product.id
        response = self.client.get(reverse('find_substitute', args=(product_id,)))
        self.assertQuerysetEqual(response.context['object_list'], ['<Product: test sub>'])

    def test_save_favorite_logged_in(self):
        old_favorite = Favorite.objects.count()
        product_id = self.product.id
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('find_substitute', args=(product_id,)), {'substitute': self.substitute.id})
        new_favorite = Favorite.objects.count()
        self.assertEqual(new_favorite, old_favorite + 1)

    def test_save_favorite_logged_off(self):
        old_favorite = Favorite.objects.count()
        product_id = self.product.id
        self.client.post(reverse('find_substitute', args=(product_id,)), {'substitute': self.substitute.id})
        new_favorite = Favorite.objects.count()
        self.assertEqual(new_favorite, old_favorite)


class FavoritePageTestCase(TestCase):
    def setUp(self):
        user = create_testing_user()
        create_testing_user(username='testuser no favorite', password='12345')
        category = Category.objects.create(name="test category")
        substitute = Product.objects.create(name="test sub", category=category, nutrition_grade="a")
        self.favorite = Favorite.objects.create(user=user, substitute=substitute)

    def test_favorite_page_no_object(self):
        self.client.login(username='testuser no favorite', password='12345')
        response = self.client.get(reverse('favorite'))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_favorite_page_with_object(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('favorite'))
        self.assertQuerysetEqual(response.context['object_list'], ['<Favorite: test sub>'])

    def test_favorite_page_302(self):
        response = self.client.get(reverse('favorite'))
        self.assertEqual(response.status_code, 302)
