from django.contrib import admin

from .models import Product, Customer,Order,Tag

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Tag)