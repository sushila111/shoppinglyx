from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app.forms import LoginForm, LogoutForm, MyPasswordResetForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from app.views import (
    ProductView,
    product_detail,
    ProductDetailView,
    add_to_cart,
    show_cart,
    plus_cart,
    buy_now,
    profile,
    address,
    orders,
    mobile,
    login,
    CustomerRegistrationView,
    checkout,
    ProfileView,
    checkout,
    payment_done,
    minus_cart,
    remove_cart
)


urlpatterns = [
    path('', ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>',
         ProductDetailView.as_view(), name='product-detail'),
         # cart path
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', show_cart, name='showcart'),
    path('pluscart/', plus_cart),
    path('minuscart/', minus_cart, name='minus-cart'),
    path('removecart/',remove_cart, name='remove-cart'),
     # related urls
    path('buy/', buy_now, name='buy-now'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/', address, name='address'),
    path('orders/', orders, name='orders'),
    path('mobile/', mobile, name='mobile'),
    path('mobile/<slug:data>', mobile, name='mobiledata'),
    path('checkout/', checkout, name='checkout'),
    #payment done 
    path('paymentdone/',payment_done, name='paymentdone'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',
         authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', CustomerRegistrationView.as_view(),
         name='customerregistration'),

    # password change related code
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html',
         form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(
        template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',
         form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    path('payment/', payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
