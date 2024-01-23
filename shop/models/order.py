from django.db import models
from .product import Product
from .customer import Customer

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Using DecimalField for price to handle decimal values
    address = models.CharField(max_length=255, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(auto_now_add=True)  # Use auto_now_add to set the date automatically on creation
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')

    def place_order(self):
        return self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

