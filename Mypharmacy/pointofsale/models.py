from django.db import models
# Create your models here.
from inventory.models import Medicine

class Sale(models.Model):
    order_id = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True, null=True)
    customer_name = models.CharField(max_length=50,default='')
    customer_phone = models.CharField(max_length=50,default='')
    payment_type = models.CharField(max_length=20,default='card')
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    tax = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    grandtotal = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    paid = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    returned = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)





class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)  # Optional
    customer_phone = models.IntegerField( blank=True, null=True)  # Optional
    # You can also add user = models.ForeignKey(User, ...) if using authentication

    def __str__(self):
        return f"Order #{self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255,default='')
    form = models.CharField(max_length=255,default='')
    unit = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    siunit = models.CharField(max_length=20,default='')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total= models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.quantity} x {self.name} @ ${self.price}"