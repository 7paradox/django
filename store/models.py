from ast import Or
from pyexpat import model
from sqlite3 import dbapi2
from django.db import models

# Create your models here.


class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')

class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

class Product(models.Model):
    # sku=models.CharField(max_length=10,primary_key=True)
    title=models.CharField(max_length=255)
    slug=models.SlugField(default='-')
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    inventory=models.IntegerField()
    last_update=models.DateField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions=models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_GOLD,'Gold'),
        (MEMBERSHIP_SILVER,'Silver')
    ]
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    eamil=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default='B')
    
    class Meta:
        db_table='store_customers'
        indexes=[
            models.Index(fields=['last_name','first_name'])
        ]

class Order(models.Model):
    placed_at=models.DateField(auto_now_add=True)
    PAYMENT_STATUS_PENDING='P'
    PAYMENT_STATUS_COMPLETE='C'
    PAYMENT_STATUS_FAILED='F'
    PAYMENT_STATUS=[
        (PAYMENT_STATUS_PENDING,"Pending"),
        (PAYMENT_STATUS_COMPLETE,"Complete"),
        (PAYMENT_STATUS_FAILED,"Failed")
    ]
    payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS,default=PAYMENT_STATUS_PENDING)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)


class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    zip=models.CharField(max_length=255)



class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    

class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,models.CASCADE)
    quantity=models.PositiveSmallIntegerField()

