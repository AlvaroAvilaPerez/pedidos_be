from django.contrib import admin
from . models import Customers
from . models import Account

# Register your models here.

admin.site.register(Customers)
admin.site.register(Account)
