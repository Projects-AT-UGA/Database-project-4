# Generated by Django 5.0.4 on 2024-04-19 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_menuitem_menu_item_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='customer_name',
            new_name='customer_user_name',
        ),
    ]
