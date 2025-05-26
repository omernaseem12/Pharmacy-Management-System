from django.contrib import admin

# Register your models here.
from .models import OrderItem,Order, Sale,Return

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Sale)
admin.site.register(Return)