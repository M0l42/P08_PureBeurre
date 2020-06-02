from purebeurre.models import Product, Category
from django.core.exceptions import ObjectDoesNotExist
import os
import json
import requests


def check_error(check_data, first_arg, second_arg):
    """
    Check if the json tags are valid
    :param check_data:
    :param first_arg:
    :param second_arg:
    :return: Value of the tags or None
    """
    try:
        if second_arg:
            return check_data[first_arg][second_arg]
        else:
            return check_data[first_arg]
    except KeyError:
        return None


def run():
    """
    Script to Load data from https://fr.openfoodfacts.org/
    Get the categories from a json files, and make a request to get the number of product of that category
    Get all the product from all the loaded category
    Put all of this in the database
    """
    headers = {"user-agent": "python-app/0.0.1"}

    current_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_path, "categories.json")

    with open(json_path, 'r') as file:
        data = json.load(file)

    print("Creating Category")
    for category in data['tags']:
        # Get the data wanted from json file
        new_category = Category.objects.get(tags=category['id'])
        # Get the number of product available in this category ( can change )
        r = requests.get(new_category.url, headers=headers)
        new_category.products = r.json()["count"]
        new_category.save()

    categories = Category.objects.all()

    print('Creating Product')

    search_url = "https://fr.openfoodfacts.org/cgi/search.pl?"

    for category in categories:
        print("Start loading product from category %s" % category.name)

        payload = {"action": "process",
                   "tagtype_0": "categories",
                   "tag_contains_0": "contains",
                   "tag_0": category.tags,
                   "page_size": 50,
                   "sort_by": "unique_scans_n",
                   "json": 1}
        for i in range(int(category.products / payload["page_size"])):
            # Get all the data wanted from the request we made
            # Get through every page of the category's product
            payload['page'] = i
            print("Loading page %d from category %s" % (i, category.name))
            r = requests.get(search_url, headers=headers, params=payload)
            data = r.json()
            for product in data["products"]:
                try:
                    new_product = Product.objects.get(code=str(product['code']))
                except ObjectDoesNotExist:
                    new_product = Product()
                    new_product.code = str(product['code'])
                new_product.name = str(check_error(product, 'product_name', ''))
                new_product.ingredients = check_error(product, 'ingredients_text_fr', '')
                new_product.url = product['url']
                new_product.img_url = check_error(product, 'image_small_url', '')

                new_product.store = check_error(product, 'stores', '')
                new_product.category = category

                new_product.nutrition_grade = check_error(product, 'nutrition_grades', '')

                new_product.salt_100 = check_error(product, 'nutriments', 'salt_100g')
                new_product.salt_lvl = check_error(product, 'nutrient_levels', 'salt')

                new_product.sugar_100 = check_error(product, 'nutriments', 'sugars_100g')
                new_product.sugar_lvl = check_error(product, 'nutrient_levels', 'sugars')

                new_product.fat_100 = check_error(product, 'nutriments', 'fat_100g')
                new_product.fat_lvl = check_error(product, 'nutrient_levels', 'fat')

                new_product.saturated_fat_100 = check_error(product, 'nutriments', 'saturated-fat_100g')
                new_product.saturated_fat_lvl = check_error(product, 'nutrient_levels', 'saturated-fat')

                new_product.save()

    print("\n Database is ready to be used")
