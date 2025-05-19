from django.db import models
import datetime
# Create your models here.

class Medicine(models.Model):
    med_id = models.AutoField(primary_key=True)
    med_brand = models.CharField(max_length=20)
    med_name = models.CharField(max_length=20)
    med_batch = models.IntegerField()
    med_dose = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    med_dose_unit = models.CharField(max_length=20,default='')
    med_expiry =models.DateField()
    med_par = models.IntegerField()
    med_stock = models.IntegerField()
    med_unitprice = models.IntegerField()
    med_boxprice = models.IntegerField()
    med_boxQ = models.IntegerField()
    med_dosage_form = models.CharField(max_length=20, default='')
    med_flag = models.BooleanField()

    def __str__(self):
        return f"Brand: {self.med_brand} - Med: {self.med_name} - Dose: {self.med_dosage_form}:{self.med_dose}{self.med_dose_unit}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_brand = models.CharField(max_length=20)
    order_name = models.CharField(max_length=20)
    order_dose = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    order_dose_unit = models.CharField(max_length=20,default='')
    order_stock = models.IntegerField()
    order_date = models.DateField(default=datetime.date.today)
    order_dosage_form = models.CharField(max_length=20,default='')
    order_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Brand: {self.order_brand} - Med: {self.order_name} - Dose: {self.order_dosage_form}:{self.order_dose}{self.order_dose_unit}"


