from django.db import models
from django.conf import settings
import os

NUTRITION_GRADES = [
    ('', 'N/A'),
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
    ('e', 'E'),
]


class Category(models.Model):
    """
    A simple model for use with ``Product`` behavior.
    Make the classification easier
    """
    name = models.CharField(verbose_name='name', max_length=200)
    tags = models.CharField(verbose_name='tags', max_length=200)
    url = models.CharField(verbose_name='url', max_length=200, blank=True)
    products = models.IntegerField(verbose_name='products', default=0, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Main model, stock all the info we'll use to our products
    """
    name = models.CharField(verbose_name='name', max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category', null=True)
    ingredients = models.TextField(verbose_name='ingredients', blank=True, null=True)
    store = models.TextField(verbose_name='store', blank=True, null=True)
    nutrition_grade = models.CharField(
        max_length=1,
        choices=NUTRITION_GRADES,
        default='',
        null=True
    )
    code = models.CharField(verbose_name="code", max_length=20, blank=True, null=True)
    url = models.TextField(verbose_name="url", blank=True, null=True)
    img_url = models.TextField(verbose_name="image_url", blank=True, null=True)

    fat_100 = models.FloatField(verbose_name="fat_100g", blank=True, default=0, null=True)
    fat_lvl = models.CharField(verbose_name="fat_lvl", blank=True, max_length=10, null=True)

    saturated_fat_100 = models.FloatField(verbose_name="saturated_fat_100g", blank=True, default=0, null=True)
    saturated_fat_lvl = models.CharField(verbose_name="saturated_fat_lvl", blank=True, max_length=10, null=True)

    sugar_100 = models.FloatField(verbose_name="sugar_100g", blank=True, default=0, null=True)
    sugar_lvl = models.CharField(verbose_name="sugar_lvl", blank=True, max_length=10, null=True)

    salt_100 = models.FloatField(verbose_name="salt_100g", blank=True, default=0, null=True)
    salt_lvl = models.CharField(verbose_name="salt_lvl", blank=True, max_length=10, null=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """
    A simple model that stock favorite product to the user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    substitute = models.ForeignKey('Product', related_name='substitute', on_delete=models.CASCADE)

    def __str__(self):
        return self.substitute.name


def photo_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    return 'purebeurre/static/assets/img/users/{username}{file_extension}'.format(
        username=instance.user.username, basename=basefilename, file_extension=file_extension)


class UserInfos(models.Model):
    """
        A model connected to the User Model to add more infos like an image ( a description in the future )
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    image = models.ImageField(upload_to=photo_path)
