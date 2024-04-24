from django.contrib import admin
from .models import Clerk, MenuItem, Cart, Order, OrderItem

# Register your models with the admin site
admin.site.register(Clerk)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(Payment)
