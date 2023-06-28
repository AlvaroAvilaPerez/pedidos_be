from django.contrib import admin
from . models import Customers, Wallet, Account


admin.site.register(Customers)
admin.site.register(Account)
admin.site.register(Wallet)
