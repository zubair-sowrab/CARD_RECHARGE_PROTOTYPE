# cards/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import check_balance, card_details, request_new_card, recharge_card, recharge_success, recharge_fail, recharge_cancel,landing_page
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.home, name='home'),
    path('check-balance/', views.check_balance, name='check_balance'),
    path('card-details/', views.card_details, name='card_details'),
    path('request-new-card/', views.request_new_card, name='request_new_card'),
    path('recharge-card/', views.recharge_card, name='recharge_card'),
    path('recharge-success/', views.recharge_success, name='recharge_success'),
    path('recharge-fail/', views.recharge_fail, name='recharge_fail'),
    path('recharge-cancel/', views.recharge_cancel, name='recharge_cancel'),
]