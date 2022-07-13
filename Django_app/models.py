from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField

# Create your models here.

#Categories for products
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#Contact Form
class ContactUs(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Subject = models.CharField(max_length=200)
    Message = models.TextField()

#Products
class Products2(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    Product_name = models.CharField(max_length=200)
    Product_desc = models.CharField(max_length=300)
    Product_price = models.IntegerField()
    Special_offer = models.BooleanField(default=False)
    Product_image = models.ImageField(upload_to='images')
    # Image_url = models.CharField(max_length=200,default=None)

    def __str__(self):
        return self.Product_name

    

    @property
    def Product_imageURL(self):
        try:
            url = self.Product_image.url
        except:
            url = ''
        return url 

    @property
    def pricecomma(self):
        ok = f'{self.Product_price:,}'
        return ok


class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   Address = models.CharField(max_length=255)
   City = models.CharField(max_length=255)
   PostalCode = models.CharField(max_length=255)
   PhoneNo = models.CharField(max_length=255,null=True)

   def __str__(self):
        return str(self.user)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    
    def __str__(self):
        return str(self.name)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) 
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total1 for item in items])
        totalwithcommas = f'{total:,}'
        return totalwithcommas
    
    @property
    def get_cart_items(self):
        items = self.orderitem_set.all()
        total = sum([item.quantity for item in items])
        return total

class OrderItem(models.Model):
    product2 = models.ForeignKey(Products2, on_delete=models.SET_NULL, blank=True, null=True)
    # product_bag = models.ForeignKey(ProductsBags, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.id)

    
    @property
    def get_total1(self):
        total = self.product2.Product_price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    phoneNo = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)

