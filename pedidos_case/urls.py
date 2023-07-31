"""pedidos_case URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views

#rutas de urls

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('customers/', views.CustomerList.as_view()),
    path('customer/<int:customer_id>/', views.CustomerOnly.as_view()),
    path('accounts/', views.AccountListView.as_view(), name='accounts-list'),
    path('account/create/', views.AccountCreate.as_view(), name='account-create'),
    path('accounts/<int:customer_id>/', views.AccountsOfACustomer.as_view(), name='account-of-a-acount'),
    path('account/<int:customer_id>/<str:account_number>/', views.AccountOnly.as_view(), name='account-only'),
    path('wallets/', views.WalletListView.as_view(), name='wallet-list'),
    path('wallet/<str:account_number>/<str:wallet_number>/', views.WalletOnly.as_view(), name='wallet-only'),
    path('wallet/create/', views.WalletCreate.as_view(), name='wallet-create'),
    path('deposit/<int:customer_id>', views.DepositInAccountOnly.as_view()),
    path('withdraw/<int:customer_id>', views.WithdrawInAccount.as_view()),
    path('login/', views.UserLogin.as_view()),
]
