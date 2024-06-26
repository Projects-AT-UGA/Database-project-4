# Generated by Django 5.0.4 on 2024-04-24 22:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_order_customer_mobile_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderContains',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.order')),
            ],
        ),
        migrations.DeleteModel(
            name='OrderedItem',
        ),
    ]
