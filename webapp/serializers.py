from rest_framework import serializers
from . models import Customers
from . models import Product
from . models import Order
from . models import Account


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
