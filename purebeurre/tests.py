from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Product, Category, Favorite


def create_testing_user(username='testuser', password='12345'):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    return user


class HomePageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class LegalMentionsPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('legal_mentions'))
        self.assertEqual(response.status_code, 200)


class AccountPageTestCase(TestCase):
    def setUp(self):
        create_testing_user()

    def test_index_page_returns_302(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_index_page_returns_200(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)


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
        # response = self.client.get()
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

    def test_save_favorite(self):
        old_favorite = Favorite.objects.count()
        product_id = self.product.id
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('find_substitute', args=(product_id,)),
                                    {'substitute': self.substitute.id})
        new_favorite = Favorite.objects.count()
        self.assertEqual(new_favorite, old_favorite + 1)


class FavoritePageTestCase(TestCase):
    def setUp(self):
        user = create_testing_user()
        create_testing_user(username='testuser no favorite', password='12345')
        category = Category.objects.create(name="test category")
        substitute = Product.objects.create(name="test sub", category=category, nutrition_grade="a")
        self.favorite = Favorite.objects.create(user=user, substitute=substitute)

    def test_search_substitute_page_no_object(self):
        self.client.login(username='testuser no favorite', password='12345')
        response = self.client.get(reverse('favorite'))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_search_substitute_page_with_object(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('favorite'))
        self.assertQuerysetEqual(response.context['object_list'], ['<Favorite: test sub>'])


class SignUpTestCase(TestCase):
    def setUp(self):
        self.form = {'username': "test",
                     "first_name": "nathan",
                     "last_name": "boukobza",
                     "email": "email@email.com",
                     "password": "123456"}

    def test_sign_up_valid(self):
        old_accounts = User.objects.count()
        self.form["confirm_password"] = "123456"
        response = self.client.post(reverse('sign_up'), self.form)
        new_accounts = User.objects.count()
        self.assertEqual(new_accounts, old_accounts + 1)

    def test_sign_up_non_valid(self):
        old_accounts = User.objects.count()
        self.form["confirm_password"] = "abcde"
        response = self.client.post(reverse('sign_up'), self.form)
        new_accounts = User.objects.count()
        self.assertEqual(new_accounts, old_accounts)


class LogInTestCase(TestCase):
    def setUp(self):
        create_testing_user()

    def test_log_in_success(self):
        response = self.client.post(reverse('login'), {"username": "testuser", "password": "12345"})
        user = auth.get_user(self.client)
        assert user.is_authenticated

    def test_log_in_failure(self):
        response = self.client.post(reverse('login'), {"username": "testuser", "password": "123456"})
        user = auth.get_user(self.client)
        assert not user.is_authenticated


class LogOffTestCase(TestCase):
    def setUp(self):
        create_testing_user()

    def test_log_off(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        user = auth.get_user(self.client)
        assert not user.is_authenticated
