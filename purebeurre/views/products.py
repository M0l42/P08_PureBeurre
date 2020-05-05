from purebeurre.models import Product, Category, Favorite
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound


class ProductView(View):
    """
    A class of View to show the details of a specific product
    ...

    Attributes
    ----------
    template_name : str
        the name of the template

    Methods
    -------
    get(self, *args, **kwargs)
        Get in the database the product and render the page

    """
    template_name = 'pure_beurre/product.html'

    def get(self, *args, **kwargs):
        """
        Get a specific product from it's ID given in the url of the page
        Put the product into the context to be able to have access to it in the template
        Render the page with the context

        Parameters
        ----------
        args : str
            Some argument that Django are passing
        kwargs : str
            Other argument that Django are passing, like our product's ID

        Returns
        -------
        HttpResponse
            a render page with all the information needed

        Raises
        ------
        ObjectDoesNotExist
            If the Id passed doesn't exist in the database
            return a 404 Page
        """
        context = dict()
        try:
            product = Product.objects.get(pk=kwargs['product'])
            context['product'] = product
            context['title'] = product.name
        except ObjectDoesNotExist:
            # Should only happened when a url is manually typed
            return HttpResponseNotFound('<h1>Page not found</h1>')

        return render(self.request, self.template_name, context=context)


class ProductSearchView(ListView):
    """
    A class of ListView to list into the page all the products containing the query's result in it name

    ...

    Attributes
    ----------
    template_name : str
        the name of the template
    model : Product
        Model of the queryset
    paginate_by : int
        Number of objects a single page should contains

    Methods
    -------
    get_context_data(self, **kwargs):
        Get the context of the view
    get_queryset(self):
        Define the queryset of the view


    """
    model = Product
    template_name = 'pure_beurre/product_search.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        """
        Call the original method of the view and add the title on the context

        Parameters
        ----------
        kwargs : str
            Some argument that Django are passing, need when call the original method of the view

        Returns
        -------
        dict
            a dict of the context of the page
        """

        context = super().get_context_data(**kwargs)
        context['title'] = 'Product searched'
        return context

    def get_queryset(self):
        """
        Get the query given from the search form in the home page or the nav bar
        Filter the product to only get products with name containing the query

        Returns
        -------
        Queryset
            a queryset of all the product filtered
        """
        search = self.request.GET['query']
        product = Product.objects.filter(name__contains=search)
        return product


class FindSubstituteView(ListView):
    """
    A class of ListView to list into the page all the substitute's product possible

    ...

    Attributes
    ----------
    template_name : str
        the name of the template
    model : Product
        Model of the queryset
    paginate_by : int
        Number of objects a single page should contains

    Methods
    -------
    get_context_data(self, **kwargs):
        Get the context of the view
    get_queryset(self):
        Define the queryset of the view

    """

    model = Product
    template_name = 'pure_beurre/substitute.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        """
        Call the original method of the view and add the title on the context

        Parameters
        ----------
        kwargs : str
            Some argument that Django are passing, need when call the original method of the view

        Returns
        -------
        dict
            a dict of the context of the page
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Substitute'
        return context

    def get_queryset(self):
        """
        Get a specific product from it's ID given in the url of the page.
        Filter the product to have only products from the same category
        Exclude the product without any nutrition grade
        And Order the queryset to have higher grades first

        Returns
        -------
        Queryset
            a queryset of all the product filtered
        """
        product = Product.objects.get(pk=self.kwargs['product'])
        category = product.category
        substitute = Product.objects.filter(category=category).exclude(nutrition_grade__isnull=True).order_by('nutrition_grade')
        return substitute

    def post(self, *args, **kwargs):
        """
        Call the original method of the view and add the title on the context

        Parameters
        ----------
        args : str
            Some argument that Django are passing
        kwargs : str
            Other argument that Django are passing

        Returns
        -------
        redirect()
            a function to redirect to a specific url
        """
        if self.request.method == "POST":
            if self.request.user.is_authenticated:
                sub = self.request.POST['substitute']
                substitute = Product.objects.get(pk=sub)
                user = self.request.user
                Favorite.objects.create(user=user, substitute=substitute)

                return redirect('/')
            else:
                return redirect('/login/')


class FavoriteView(LoginRequiredMixin, ListView):
    """
    A class of ListView to list into the page all the user's favorite product
    Must be loged on to access this page

    ...

    Attributes
    ----------
    template_name : str
        the name of the template
    model : Favorite
        Model of the queryset
    paginate_by : int
        Number of objects a single page should contains
    login_url : str
        The url of the login page

    Methods
    -------
    get_context_data(self, **kwargs):
        Get the context of the view
    get_queryset(self):
        Define the queryset of the view
    """

    login_url = '/login/'
    model = Favorite
    template_name = 'pure_beurre/favorite.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        """
        Call the original method of the view and add the title on the context

        Parameters
        ----------
        kwargs : str
            Some argument that Django are passing, need when call the original method of the view

        Returns
        -------
        dict
            a dict of the context of the page
        """

        context = super().get_context_data(**kwargs)
        context['title'] = 'Favoris'
        return context

    def get_queryset(self):
        """
        Get the current user
        Get all the favorite product of the user

        Returns
        -------
        Queryset
            a queryset of all the favorite product from the user
        """
        user = self.request.user
        return Favorite.objects.filter(user=user)
