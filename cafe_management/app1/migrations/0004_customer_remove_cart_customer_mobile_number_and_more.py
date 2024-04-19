# Generated by Django 5.0.4 on 2024-04-19 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_rename_customer_name_cart_customer_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='customer_mobile_number',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='customer_user_name',
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.customer'),
        ),
    ]