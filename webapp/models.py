from django.db import models


class Customers(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250, default='Sin Direccion')
    phone = models.CharField(max_length=25, default='Ninguno')
    customer_id = models.IntegerField()

    def __str__(self):
        return str(self.id) + ' - ' + self.first_name + ' ' + self.last_name


class Account(models.Model):
    customer_id = models.IntegerField()
    account_number = models.CharField(max_length=100)
    balance = models.CharField(max_length=100)

    def __str__(self):
        user_owner = Customers.objects.get(customer_id=self.customer_id)
        return str(self.id) + ' - User: ' + str(self.customer_id) + " - " + user_owner.first_name + ': Account Number: ' + str(self.account_number)
    

class Wallet(models.Model):
    wallet_number = models.CharField(max_length=100)
    balance = models.CharField(max_length=100)
    account_number =  models.CharField(max_length=100)
    beneficiary_id = models.IntegerField(max_length=250)    

    def __str__(self):
        return str(self.id) + '-' + str(self.wallet_number)