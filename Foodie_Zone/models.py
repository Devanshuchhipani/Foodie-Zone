from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,User

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Table"

# Create your models here.
class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="team")
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def image(self):
        return self.logo
    
    
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_id = models.CharField(max_length=10,primary_key=True)
    restaurant_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    contact_no = models.IntegerField()
    contract_duaration = models.IntegerField(default=12,null=True)
    profit_share = models.IntegerField()
    res_image = models.ImageField(upload_to='img',null=True)

class Items(models.Model):
    Rest = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='item',null=True)
    ingredients = models.TextField()
    price = models.FloatField()
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"item name : {self.name}, Rest : {self.Rest}"
    
    def get_rest(self):
        return self.Rest 

    class Meta:
        verbose_name_plural ="Item Table"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=10,primary_key=True)
    customer_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    mobile_no = models.IntegerField()
    profile_pic = models.ImageField(upload_to="customer",null=True)

    def __str__(self):
        return self.customer_name 

    class Meta:
        verbose_name_plural ="Customer Table"

class Report(models.Model):
    us_id = models.CharField(max_length=15)
    us_name = models.CharField(max_length=20)
    us_email = models.EmailField(max_length=20)
    subject = models.CharField(max_length=25)
    prob_whom = models.CharField(max_length=20)
    problem = models.CharField(max_length=200)

    def __str__(self):
        return self.us_name

import uuid

def generate_unique_key():
    return str(uuid.uuid4())
   
class Cart(models.Model):
    id1 = models.IntegerField(primary_key=True,unique=True)
    session_key = models.CharField(max_length=32,blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart id1 = {self.id1} (session {self.session_key})"
    
class CartItem(models.Model):
    cart1 = models.ForeignKey(Cart, on_delete=models.CASCADE)
    Cust = models.ForeignKey(Customer,on_delete=models.CASCADE)
    item = models.ManyToManyField(Items, through='CartItem_Item')
    
    def __str__(self):
        return f"CartItem - Cart: {self.cart1.session_key}, Customer: {self.Cust},Item: {self.item.name}"
    
    
class CartItem_Item(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_quantity(self):
        return self.quantity
    
    def __str__(self):
        return f"CartItem_Item - CartItem: {self.cart_item}, Item: {self.item.name}, Item_id : {self.item.id} Quantity: {self.quantity}"
    
    def get_total_price(self):
        return self.item.price * self.quantity
    
class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('1', 'Online Payment'),
        ('2', 'COD')
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default='1')

    def __str__(self):
        return f'Payment of {self.amount} made by {self.customer} via {self.get_payment_mode_display()}'
    

class Order(models.Model):
    STAT_CHOICES = (
        ('1', 'Ordering'),
        ('2', 'Ordered'),
        ('3', 'In kitchen'),
        ('4', 'Out for delivery'),
        ('5', 'Delivered')
    )

    PAY_CHOICES = (
        ('1', 'Pending'),
        ('2', 'Paid')
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    cart_item = models.ForeignKey(CartItem, on_delete=models.PROTECT)
    paym = models.ForeignKey(Payment, on_delete=models.PROTECT, null=True)
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STAT_CHOICES, default='1')
    payment_status = models.CharField(max_length=1, choices=PAY_CHOICES, default='1')
    add = models.TextField(max_length=100,null=True)
    name = models.CharField(max_length=50,null=True)
    mo_no = models.IntegerField(null=True)


    def __str__(self):
        return f'Order {self.id} by {self.customer} at {self.order_time} ({self.get_status_display()}, {self.get_payment_status_display()}) - Delivery address: {self.add}, Name: {self.name}, Phone number: {self.mo_no}'

    
    