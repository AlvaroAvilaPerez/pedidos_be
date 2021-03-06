import json

from django.shortcuts import render

from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Customers, Order
from . models import Product
from . serializers import CustomersSerializer
from . serializers import ProductSerializer
from . serializers import OrderSerializer


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
            # return HttpResponse(status=200)
            responseData = {
                'id': user.id,
                'name': user.first_name,
                'last_name': user.last_name
                # 'is_staff': user.is_staff
            }
            if user.is_staff:
                return HttpResponse(json.dumps(responseData), content_type="application/json", status=202)

            return HttpResponse(json.dumps(responseData), content_type="application/json")
        else:
            print('User was NOT LOGGED IN')
            return HttpResponse(status=404)


class ProductList(APIView):

    def get(self, request):
        products = Product.objects.all() #obtener todas las instancias de customers
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.method == 'POST':
            received_json_data = json.loads(request.body)
            new_product = Product(name=received_json_data['name'],
                                  price=received_json_data['price'])
            new_product.save()
        return HttpResponse(status=201)


class ProductOnly(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            serializer = ProductSerializer(instance=product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            raise Http404("Product not available")

    def post(self, request):
        pass


class OrderList(APIView):
    def get(self, request):
        orders = Order.objects.all()
        orders_filtered = {}
        for orderReceived in orders:
            if not orderReceived.is_delivered:
                current_key = "" + orderReceived.customer_id + "-" + orderReceived.date + "-" + orderReceived.time
                orders_filtered[current_key] = []
                for orderFiltered in orders:
                    key_to_review = "" + orderFiltered.customer_id + "-" + orderFiltered.date + "-" + orderFiltered.time
                    if key_to_review == current_key:
                        orders_filtered[current_key].append(orderFiltered)

        json_response = []
        for eachElement in orders_filtered.values():
            customer_id = ""
            address = ""
            date = ""
            time = ""
            is_delivered = False
            order_receive_items = []
            items = []

            for eachOrder in eachElement:
                customer_id = eachOrder.customer_id
                date = eachOrder.date
                time = eachOrder.time
                product = Product.objects.get(pk=eachOrder.product_id)
                is_delivered = eachOrder.is_delivered
                order_receive_item = {
                    "product_id": eachOrder.product_id,
                    "product_name": product.name,
                    "product_price": product.price,
                    "quantity": eachOrder.quantity
                }
                order_receive_items.append(order_receive_item)

            for each_order_receive_item in order_receive_items:
                items.append(each_order_receive_item)

            customer = Customers.objects.get(customer_id=customer_id)
            json_element = {
                           "customer_id": customer_id,
                           "address": customer.address,
                           "customer_name": customer.first_name,
                           "customer_last_name": customer.last_name,
                           "is_delivered": is_delivered,
                           "date": date,
                           "time": time,
                           "items": items
                          }
            json_response.append(json_element)
        return JsonResponse(json_response, safe=False)


class OrderDetail(APIView):
    def post(self, request):
        if request.method == 'POST':
            received_json_data = json.loads(request.body)

            for productItem in received_json_data['items']:
                product = Product.objects.get(pk=productItem['productId'])

                calculated_price = int(productItem['quantity']) * int(product.price)
                new_order = Order(product_id=productItem['productId'],
                                  customer_id=received_json_data['customer'],
                                  quantity=productItem['quantity'],
                                  date=received_json_data['date'],
                                  time=received_json_data['time'],
                                  Price=calculated_price,
                                  is_delivered=False)
                new_order.save()

        return HttpResponse(status=201)


class OrderDeliveredUpdate(APIView):

    def post(self, request):
        orders = Order.objects.all()
        received_json_data = json.loads(request.body)
        orders_filtered = {}
        for orderReceived in orders:
            current_key = "" + orderReceived.customer_id + "-" + orderReceived.date + "-" + orderReceived.time
            orders_filtered[current_key] = []
            for orderFiltered in orders:
                key_to_review = "" + orderFiltered.customer_id + "-" + orderFiltered.date + "-" + orderFiltered.time
                if key_to_review == current_key:
                    orders_filtered[current_key].append(orderFiltered)
        orders_key = "" + received_json_data['customer_id'] + "-" + received_json_data['date'] + "-" + received_json_data['time']
        for order_to_update in orders_filtered[orders_key]:
            print(order_to_update)
            order_to_update.is_delivered = True
            order_to_update.save()
        return HttpResponse(status=200)
