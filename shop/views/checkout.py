from django.shortcuts import render, redirect
from django.views import View
from shop.models.product import Product
from shop.models.order import Order
from shop.models.customer import Customer
class Checkout(View):
    def post(self, request):
        # Extract data from the form
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer_id = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        # Create orders and save to the database
        for product in products:
            order = Order(
                customer=Customer(id=customer_id),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id)),
                status = 'paid',
            )
            request.session['cart'] = {}
            order.save()

        # Redirect to the orders page or any other desired page
        return redirect('orders')
