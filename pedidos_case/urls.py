from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from webapp import views

#rutas de urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', views.CustomerList.as_view()),
    path('customer/<int:customer_id>', views.CustomerOnly.as_view()),
    path('accounts/', views.AccountList.as_view()),
    path('accounts/<int:customer_id>', views.AccountOnly.as_view()),
    path('accounts/<int:customer_id>/<str:account_number>', views.AccountOnly.as_view()),
    path('deposit/<int:customer_id>', views.DepositInAccountOnly.as_view()),
    path('wallets/', views.WalletsList.as_view()),
    path('withdraw/<int:customer_id>', views.WithdrawInAccount.as_view()),
    path('login/', views.UserLogin.as_view()),
]
