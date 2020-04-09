from django.urls import path
from .views import HomeView
from .views.products import ProductView, ProductByCategoryView, SaveSubstituteView, FindSubstituteView, FavoriteView
from .views.login import LogInFormView, SignUpFormView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('product/', ProductView.as_view(), name='product'),
    path('product/<category>/', ProductByCategoryView.as_view(), name='sort_product'),
    path('product/<category>/<int:product>/', FindSubstituteView.as_view(), name='find_substitute'),
    path('product/<category>/<int:product>/<int:substitute>', SaveSubstituteView.as_view(), name='save_favorite'),

    path('favorite', FavoriteView.as_view(), name='favorite'),

    path('sign_up/', SignUpFormView.as_view(), name='create-user'),
    path('login/', LogInFormView.as_view(), name='login'),
]
