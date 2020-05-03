from purebeurre.models import Product, Category, Favorite
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
import logging

logger = logging.getLogger(__name__)


class ProductView(View):
    template_name = 'pure_beurre/product.html'

    def get(self, request, *args, **kwargs):
        context = dict()


        try:
            product = Product.objects.get(pk=kwargs['product'])
            context['product'] = product
            context['title'] = product.name
        except ObjectDoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return render(self.request, self.template_name, context=context)


class ProductSearchView(ListView):
    model = Product
    template_name = 'pure_beurre/product_search.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Product searched'
        return context

    def get_queryset(self):
        search = self.request.GET['query']
        product = Product.objects.filter(name__contains=search)
        return product


class FindSubstituteView(ListView):
    model = Product
    template_name = 'pure_beurre/substitute.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Substitute'
        context['product'] = Product.objects.get(pk=self.kwargs['product'])
        return context

    def get_queryset(self):
        product = Product.objects.get(pk=self.kwargs['product'])
        category = product.category
        substitute = Product.objects.filter(category=category).exclude(nutrition_grade__isnull=True).order_by('nutrition_grade')
        return substitute

    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            sub = self.request.POST['substitute']
            product = Product.objects.get(pk=kwargs['product'])
            substitute = Product.objects.get(pk=sub)
            user = self.request.user
            Favorite.objects.create(user=user, substitute=substitute)

            return redirect('/')


class FavoriteView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Favorite
    template_name = 'pure_beurre/favorite.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Favoris'
        return context

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)
