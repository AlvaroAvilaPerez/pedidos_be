import json

from django.shortcuts import render

from django.http import HttpResponse, Http404, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customers, Account
from .serializers import CustomersSerializer, AccountSerializer
from rest_framework.exceptions import PermissionDenied



class CustomerList(APIView):
    def get(self, request):
        customers1 = Customers.objects.all() #obtener todas las instancias de customers
        serializer = CustomersSerializer(customers1, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.method == 'POST':
            received_json_data = json.loads(request.body)
            print(received_json_data['user'])
            print(received_json_data['password'])

            new_customer_user = User.objects.create_user(username=received_json_data['user'],
                                                    email=received_json_data['email'],
                                                    first_name=received_json_data['first_name'],
                                                    last_name=received_json_data['last_name'],
                                                    password=received_json_data['password'])
            new_customer_user.save()
            new_customer = Customers(first_name=received_json_data['first_name'],
                                     last_name=received_json_data['last_name'],
                                     address=received_json_data['address'],
                                     phone=received_json_data['phone'],
                                     customer_id=new_customer_user.id)
            new_customer.save()
        return HttpResponse(status=201)


class AccountList(APIView):
    def get(self, request):
        accounts = Account.objects.all() #obtener todas las instancias de Accounts
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.method == 'POST':
            received_json_data = json.loads(request.body)
            print(received_json_data['customer_id'])
            print(received_json_data['account_number'])
            print(received_json_data['balance'])
            # read customer_id from the token in the future
            new_account = Account(customer_id=received_json_data['customer_id'],
                                  account_number=received_json_data['account_number'],
                                  balance=received_json_data['balance'])
            new_account.save()
        return HttpResponse(status=201)
    

class CustomerOnly(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customers.objects.get(customer_id=customer_id)
            serializer = CustomersSerializer(instance=customer)
            return Response(serializer.data)
        except Customers.DoesNotExist:
            raise PermissionDenied("Customer does not exist")

    def delete(self, request, customer_id):
        try:        
            accounts = Account.objects.filter(customer_id=customer_id)
            customer = Customers.objects.filter(customer_id=customer_id)
            user = User.objects.filter(id=customer_id)

            if not accounts.exists() and not customer.exists() and not user.exists():
                raise PermissionDenied("Customer does not exist")

            for account in accounts:
                account.delete()                       
            customer.delete()
            user.delete()

            return HttpResponse(status=200)
        except Account.DoesNotExist:
            raise PermissionDenied("Customer does not exist")
        

class AccountOnly(APIView):
    def get(self, request, customer_id):
        try:
            account = Account.objects.filter(customer_id=customer_id)
            if not account.exists():
                raise PermissionDenied("Account does not exist")
            
            serializer = AccountSerializer(instance=account, many=True)
            return Response(serializer.data)
        except Account.DoesNotExist:
            raise PermissionDenied("Account does not exist")
        
    def delete(self, request, customer_id, account_number):
        try:
            account = Account.objects.filter(customer_id=customer_id, account_number=account_number)
            if not account.exists():
                raise PermissionDenied("Account does not exist")

            account.delete()
            return HttpResponse(status=200)
        except Account.DoesNotExist:
            raise PermissionDenied("Account does not exist")
        

class DepositInAccountOnly(APIView):
    def post(self, request, customer_id):
        try:
            received_json_data = json.loads(request.body)
            account_number = received_json_data['account_number']
            deposit_to_do = float(received_json_data['deposit'])
            deposit_limit = 10000
            if deposit_to_do > deposit_limit:
                return HttpResponse(status=400, reason="Deposit Limit is exceeded, deposits should be under 10,000")
            account = Account.objects.get(customer_id=customer_id, account_number=account_number)
            account.balance = str(float(account.balance) + deposit_to_do)
            account.save()
            serializer = AccountSerializer(instance=account, many=False)
            return Response(serializer.data)
        except Account.DoesNotExist:
            raise Http404("Account does not Exist")
        
    
class WithdrawInAccount(APIView):
    def is_transaction_valid(current_balance, withdraw_to_do):
        limit_porcentual_threshold = 90
        balance_limit = 100
        if current_balance > withdraw_to_do:
            withdraw_to_do_porcentual = ((withdraw_to_do * 100) / current_balance) 
            if withdraw_to_do_porcentual <= limit_porcentual_threshold:   
                balance = (current_balance - withdraw_to_do)
                if balance >= balance_limit:
                   return True
                else:
                    return False
            else:
                return False
        else:
            return False
        

    def post(self, request, customer_id):
        try:
            received_json_data = json.loads(request.body)
            account_number = received_json_data['account_number']
            withdraw_to_do = float(received_json_data['withdraw'])
            account = Account.objects.get(customer_id=customer_id, account_number=account_number)            
            current_balance = float(account.balance)            
            if self.is_transaction_valid(current_balance, withdraw_to_do):
                account = Account.objects.get(customer_id=customer_id, account_number=account_number)
                account.balance = str(current_balance - withdraw_to_do)
                account.save()
                serializer = AccountSerializer(instance=account, many=False)
                return Response(serializer.data)
                
            else:
                return HttpResponse(status=200, reason="The account cannot have less than $100 in balance, bad transaction.")
        except Account.DoesNotExist:
            raise Http404("Account does not Exist")  
          

class UserLogin(APIView):
    def post(self, request):
        if request.method == 'POST':
            received_json_data = json.loads(request.body)
            print(received_json_data['user'])
            print(received_json_data['password'])
        # example of Login
        user = authenticate(username=received_json_data['user'], password=received_json_data['password'])
        if user is not None:
            print('El usuario ha sido loggeado')
            print(user.first_name)
            print(user.email)
            print(user.is_staff)

            responseData = {
                'id': user.id,
                'name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff
            }
            if user.is_staff:
                return HttpResponse(json.dumps(responseData), content_type="application/json", status=202)

            return HttpResponse(json.dumps(responseData), content_type="application/json")
        else:
            print('User was NOT LOGGED IN')
            return HttpResponse(status=404)
