# Generated by Django 5.0.4 on 2024-04-19 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_customer_remove_cart_customer_mobile_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='user_name',
            new_name='customer_user_name',
        ),
    ]
