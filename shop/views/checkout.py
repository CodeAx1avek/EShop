from django.shortcuts import render, redirect
from django.views import View
from shop.models.product import Product
from shop.models.order import Order
from shop.models.customer import Customer
from razorpay import Client
from Ecomm.settings import KEY,SECRET_KEY
class Checkout(View):
    def post(self, request):
        # Extract data from the form
        address = "razd"
        phone = "8448585854"
        customer_id = request.session.get('customer')
        cart = request.session.get('cart')

        # Get products in the cart
        products = Product.get_product_by_id(list(cart.keys()))

        # Create orders and save to the database
        for product in products:
            order = Order(
                customer=Customer(id=customer_id),
                product=product,
                price=product.price,
                address=address,
                phone=phone,
                quantity=cart.get(str(product.id))
            )
            order.save()

        # Clear the cart in the session after completing the orders
        request.session['cart'] = {}

        # Process Razorpay payment response
        if request.POST.get('razorpay_payment_id'):
            payment_id = request.POST.get('razorpay_payment_id')

            # Verify the payment with Razorpay
            client = Client(auth=(KEY,SECRET_KEY))
            payment_info = client.payment.fetch(payment_id)

            # Check if the payment is successful
            if payment_info['status'] == 'captured':
                # Update order status or perform other necessary actions
                # For example, you can mark the orders as paid
                for product in products:
                    order = Order.objects.filter(product=product).last()
                    order.status = 'paid'
                    order.save()

                # Redirect to a success page or any other desired page
                return redirect('success_page')

        # Redirect to the orders page or any other desired page
        return redirect('orders')
