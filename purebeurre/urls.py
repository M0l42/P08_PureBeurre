from django.urls import path
from .views import home_view, legal_mentions
from .views.products import ProductView, ProductSearchView, FindSubstituteView, FavoriteView
from .views.user import LogInFormView, SignUpFormView, LogOutView, AccountView, EditAccountFormView

urlpatterns = [
    path('', home_view, name='home'),
    path('mentions-legals', legal_mentions, name="legal_mentions"),

    path('product/', ProductSearchView.as_view(), name='product_search'),
    path('product/<int:product>/', ProductView.as_view(), name='product'),
    path('substitute/<int:product>/', FindSubstituteView.as_view(), name='find_substitute'),

    path('favorite/', FavoriteView.as_view(), name='favorite'),

    path('sign_up/', SignUpFormView.as_view(), name='sign_up'),
    path('login/', LogInFormView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('edit-account/', EditAccountFormView.as_view(), name='edit-account'),
]
