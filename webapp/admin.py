from django.contrib import admin
from . models import Customers
from . models import Product
from . models import Order
from . models import Account

# Register your models here.

admin.site.register(Customers)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Account)
