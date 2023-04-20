from django.db import models
from django.contrib.auth.models import User


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


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id) + ' - ' + self.name


class Order(models.Model):
    product_id = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    Price = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        product = Product.objects.get(id=self.product_id)
        user = User.objects.get(id=self.customer_id)
        customer = Customers.objects.get(customer_id=user.id)
        return str(self.id) + ' - ' + self.date + ' - ' + self.time + ' - Pidio: ' + self.quantity + ' - ' + product.name + ' - ' + customer.first_name
