import json

from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customers, Account, Wallet
from .serializers import CustomersSerializer, AccountSerializer, WalletSerializer


class CustomerList(APIView):
    def get(self, request):
        customers1 = Customers.objects.all()
        serializer = CustomersSerializer(customers1, many=True)
        return Response(serializer.data)

    def post(self, request):
        received_json_data = json.loads(request.body)
        email = received_json_data['email'].strip().lower()
        if User.objects.filter(username=received_json_data['user']).first():
            return HttpResponse(status=400, reason="User Name already exists")
        if User.objects.filter(email=email).exists():
            return HttpResponse(status=400, reason="Email already exists")
        else:
            new_customer_user = User.objects.create_user(username=received_json_data['user'],
                                                    email=email,
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


class AccountListView(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
    

class AccountCreate(APIView):
    def post(self, request):
        if request.method == 'POST':
            received_json_data = json.loads(request.body)
            customer_id = received_json_data['customer_id']
            account_number = received_json_data['account_number']

            customer = Account.objects.filter(customer_id=customer_id)
            if customer.exists():
                account = Account.objects.filter(account_number=account_number)
                if account.exists():
                    raise Http404("The requested Account already exists.")
            else:
                new_account = Account(customer_id=customer_id,
                                     account_number=account_number)
                new_account.save()
                return HttpResponse(status=201)
            
    
class AccountsOfACustomer(APIView):
    def get(self, request, customer_id):
        try:
            account = Account.objects.filter(customer_id=customer_id)
            
            if not account.exists():
                raise Http404 ("The requested Account was not found.")
            
            serializer = AccountSerializer(instance=account, many=True)
            return Response(serializer.data)
        
        except Account.DoesNotExist:
            raise Http404 ("The requested Account was not found.")


class AccountOnly(APIView):
    def get(self, request,customer_id, account_number):
        try:
            account = Account.objects.filter(customer_id=customer_id, account_number=account_number)

            if not account.exists():
                raise Http404 ("The requested Account was not found.")
            
            serializer = AccountSerializer(instance=account, many=True)
            return Response(serializer.data)
        
        except Account.DoesNotExist:
            raise Http404 ("The requested Account was not found.")

    def delete(self, request, customer_id, account_number):
        try:
            customer= Account.objects.filter(customer_id=customer_id)
            account = Account.objects.filter(account_number=account_number)
            
            if not customer.exists() or not account.exists() :
                raise Http404 ("The requested Account was not found.")
            else:
                account.delete()
                return HttpResponse(status=200)
            
        except Account.DoesNotExist:
            raise Http404 ("The requested Account was not found.")
        

class WalletsList(APIView):
    def get(self, request):
        wallet = Wallet.objects.all()
        serializer = WalletSerializer(wallet, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.method == 'POST':
            received_json_data = json.loads(request.body)
            account = Account.objects.filter(account_number = received_json_data['account_number'])
            if not account.exists():
                raise Http404 ("The requested Wallet was not found.")
            else:
                new_wallet = Wallet(account_number=received_json_data['account_number'],
                                    wallet_number=received_json_data['wallet_number'],
                                    balance=0)      
                new_wallet.save()
                return HttpResponse(status=201)
    

class CustomerOnly(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customers.objects.get(customer_id=customer_id)
            serializer = CustomersSerializer(instance=customer)
            return Response(serializer.data)
        except Customers.DoesNotExist:
            raise Http404 ("The requested Customer was not found.")

    def delete(self, request, customer_id):
        try:        
            accounts = Account.objects.filter(customer_id=customer_id)
            customer = Customers.objects.filter(customer_id=customer_id)
            user = User.objects.filter(id=customer_id)

            if not accounts.exists() and not customer.exists() and not user.exists():
                raise Http404 ("The requested Customer was not found.")

            for account in accounts:
                account.delete()                       
            customer.delete()
            user.delete()

            return HttpResponse(status=200)
        except Account.DoesNotExist:
            raise Http404 ("The requested Customer was not found.")
        

class WalletOnly(APIView):
    def get(self, request, account_number):
        try:
            wallet = Wallet.objects.filter(account_number=account_number)
            if not wallet.exists():
                raise Http404 ("The requested Wallet was not found.")
            serializer=WalletSerializer(instance=wallet, many=True)
            return Response(serializer.data)
        except Wallet.DoesNotExist:
            raise Http404 ("The requested Account was not found.")

    def delete(self, request, account_number, wallet_number):
        try:
            wallet = Wallet.objects.filter(account_number=account_number, wallet_number=wallet_number)
            if not wallet.exists():
                raise Http404 ("The requested Wallet was not found.")
            wallet.delete()
            return HttpResponse(status=200)
        except Account.DoesNotExist:
            raise Http404 ("The requested Wallet was not found.") 


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
            raise Http404 ("The requested Account was not found.")
        
    
class WithdrawInAccount(APIView):
    def is_transaction_valid(self, current_balance, withdraw_to_do):
        limit_porcentual_threshold = 90
        balance_limit = 100
        if current_balance >= withdraw_to_do:
            withdraw_to_do_porcentual = (withdraw_to_do * 100) / current_balance
            if withdraw_to_do_porcentual <= limit_porcentual_threshold and (current_balance - withdraw_to_do) >= balance_limit:
                return True
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
                return HttpResponse(status=400, reason="The account cannot have less than $100 in balance or exceed the withdrawal limit.")
        except Account.DoesNotExist:
            raise Http404 ("The requested Account was not found.")
          

class UserLogin(APIView):
    def post(self, request):
        if request.method == 'POST':
            received_json_data = json.loads(request.body)
        user = authenticate(username=received_json_data['user'], password=received_json_data['password'])
        if user is not None:
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
            return HttpResponse(status=404)
