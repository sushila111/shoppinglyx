from django.urls import path
from app.views import *

urlpatterns = [
    path('',home),
    path('product-detail/',product_detail,name='product-detail'),
    path('cart/',add_to_cart, name='add-to-cart'),
    path('buy/',buy_now, name='buy-now'),
    path('profile/',profile,name='profile'),
    path('address/',address,name='address'),
    path('orders/',orders,name='orders'),
    path('changepassword/',change_password,name='changepassword'),
    path('mobile/',mobile,name='mobile'),
    path('checkout/',checkout,name='checkout'),
    path('login/',login,name='login'),
    path('customerregistration/',customerregistration,name='customerregistration'),


]
