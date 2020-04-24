from django.urls import path
from .views import HomeView, AccountView
from .views.products import ProductView, ProductSearchView, SaveSubstituteView, FindSubstituteView, FavoriteView
from .views.login import LogInFormView, SignUpFormView, LogOutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('account/', AccountView.as_view(), name='account'),

    path('product/', ProductSearchView.as_view(), name='product_search'),
    path('product/<int:product>/', ProductView.as_view(), name='product'),
    path('substitute/<int:product>/', FindSubstituteView.as_view(), name='find_substitute'),
    path('substitute/<int:product>/<int:substitute>', SaveSubstituteView.as_view(), name='save_favorite'),

    path('favorite/', FavoriteView.as_view(), name='favorite'),

    path('sign_up/', SignUpFormView.as_view(), name='sign_up'),
    path('login/', LogInFormView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
]
