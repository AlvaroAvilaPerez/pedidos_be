from django.db import models


class Customers(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=250, default='No Address')
    phone = models.CharField(max_length=25, default='None')
    customer_id = models.IntegerField()

    def __str__(self):
        return str(self.id) + ' - ' + self.first_name + ' ' + self.last_name


class Account(models.Model):
    customer_id = models.IntegerField()
    account_number = models.CharField(max_length=100)
    balance = models.CharField(max_length=100, default=0)

    def __str__(self):
        return str(self.id) + ' - Customer_Id: ' + str(self.customer_id) + ': Account Number: ' + str(self.account_number) + ' Balance: ' + str(self.balance)
    

class Wallet(models.Model):
    account_number = models.CharField(max_length=50)
    wallet_number = models.CharField(max_length=50)
    beneficiary_id = models.CharField(max_length=100, null=True)
    balance = models.CharField(max_length=100, default=0) 

    def __str__(self):
        return str(self.id) + '-' + str(self.wallet_number)
