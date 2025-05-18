from django.contrib import admin

# Register your models here.
from .models import Medicine,Order

admin.site.register(Medicine)
admin.site.register(Order)

