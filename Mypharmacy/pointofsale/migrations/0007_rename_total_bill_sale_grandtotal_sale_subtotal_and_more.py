# Generated by Django 5.2.1 on 2025-05-25 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointofsale', '0006_orderitem_sub_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='total_bill',
            new_name='grandtotal',
        ),
        migrations.AddField(
            model_name='sale',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='sale',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
