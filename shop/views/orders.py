from django.shortcuts import render,redirect
from django.views import View
from shop.models.product import Product
from shop.models.order import Order
from shop.models.customer import Customer   


class OrderView(View):
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request,'orders.html',{'orders':orders})