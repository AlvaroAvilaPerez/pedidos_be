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
from webapp import views

#rutas de urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customer/create/', views.CustomerCreate.as_view(), name='customer-create'),
    path('customer/<int:customer_id>', views.CustomerDetail.as_view(), name='customer-detail'),
    path('accounts/', views.AccountListView.as_view(), name='accounts-list'),
    path('account/create/', views.AccountCreate.as_view(), name='account-create'),
    path('account/<int:account_id>', views.AccountDetail.as_view(), name='account-detail-by-number'),
    path('wallets/', views.WalletListView.as_view(), name='wallet-list'),
    path('wallet/create/', views.WalletListView.as_view(), name='wallet-create'),
    path('wallet/<int:wallet_id>', views.WalletCreate.as_view(), name='wallet-create'),
    path('deposit/<int:account_id>', views.DepositInAccount.as_view(), name='account_id-deposit'),
    path('withdraw/<int:account_id>', views.WithdrawInAccount.as_view(), name='account_id-withdraw'),
    path('login/', views.UserLogin.as_view()),
]
