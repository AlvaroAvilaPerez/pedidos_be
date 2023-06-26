from rest_framework import serializers
from . models import Customers, Wallet, Account

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Wallet
        fields = '__all__'
