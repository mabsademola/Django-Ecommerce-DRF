from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils import timezone 
import uuid
import os
from  django.conf import settings


@deconstructible
class ProductImagePath(object):
    def __init__(self):
        pass
    def __call__(self, instance, filename):
        namee, ext =  os.path.splitext(filename)
        path = f'products/{instance.id}/image'
        name= f'{instance.id}.{ext}'
        return os.path.join(path,name)
    

@deconstructible
class ProductImageListPath(object):
    def __init__(self):
        pass
    def __call__(self, instance, filename):
        namee, ext =  os.path.splitext(filename)
        path = f'products/{instance.product.id}/image/imagelist'
        name= f'{instance.product.id}_list.{ext}'
        return os.path.join(path,name)    
    
product_image_list_path = ProductImageListPath()

product_image_path = ProductImagePath()

class Review(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name = "reviews")
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.description

class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4,editable=False, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL,null=True, blank=True, related_name='products')
    image = models.ImageField(upload_to=product_image_path,blank=True,null=True)
    discount = models. BooleanField(default=False)
    price = models.FloatField(null=False,blank=False,default=0.0)
    discount_price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
   


    @property
    def percentage_discount(self):
        if self.discount_price != 0.0 and self.discount:
            percentageno = 100 - round((self.discount_price / self.price) * 100)
            percentage = '{}%'.format(percentageno)
            if percentage != 0.0:
                return percentage
            return
        else:
            return 

        
    def save(self, *args, **kwargs):
        # Check if discount_price is empty (None)
        if self.discount_price is None or self.discount_price == 0:
            self.discount_price = self.price

           # Check if discount_price is empty (None)
        if self.discount_price == self.price:
            self.discount = False

        self.last_update = timezone.now()

        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f'{self.name}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='images')
    image = models.ImageField(upload_to=product_image_list_path,blank=True,null=True)
    


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    


class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Cart Item"
    
    # def __str__(self):
    #     return str(self.id)
    
    # def sub_total(self):
    #     return self.quantity * self.product.price
        


class Order(models.Model):
    
    
    PAYMENT_STATUS_PENDING = 'Pending'
    PAYMENT_STATUS_COMPLETE = 'Complete'
    PAYMENT_STATUS_FAILED = 'Failed'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.pending_status
    
    @property 
    def total_price(self):
        items = self.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name = "items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    

    def __str__(self):
        return self.product.name





 
 