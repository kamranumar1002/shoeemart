from django.contrib import admin
from .models import Category,Products2,UserProfile,Customer,Order,OrderItem,ShippingAddress,ContactUs

# Register your models here.

admin.site.register(Products2)
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(ContactUs)