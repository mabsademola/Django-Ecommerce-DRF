from rest_framework import serializers
from categories.serializers import *
from .serializers import *
from django.db import transaction
from .models import *

class ProductImageSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = ProductImage
        fields = ['url','product','image']


class ProductSerializer(serializers.ModelSerializer):
 
    images= ProductImageSerializer(many=True, read_only=True,)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=10000000,allow_empty_file=False,use_url=False), write_only=True,
    )
    class Meta:
        model = Product
        fields = ['url','name','description','image','images','price','percentage_discount','discount_price', 'discount','uploaded_images']
    
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
          new_image =  ProductImage.objects.create(product=product, image=image)
          new_image.save()
          
   
        return product


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date_created", "name", "description"]
    
  
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id = product_id,  **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            # 'url',
                  "id",
                  "name", "price"]
        
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        
        return value
    
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"] 
        quantity = self.validated_data["quantity"] 
        
        try:
            cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()         
            self.instance = cartitem     
        except:
            self.instance = Cartitems.objects.create(cart_id=cart_id, **self.validated_data)           
            return self.instance
  
         

    class Meta:
        model = Cartitems
        fields = ['url',"id", "product_id", "quantity"]

class UpdateCartItemSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cartitems
        fields = ["quantity"]
        

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField( method_name="total")
    class Meta:
        model= Cartitems
        fields = [
            # 'url',
            "id", 
            
                  "cart",
                   "product", 
                   "quantity", 
                   "sub_total",
                   ]
        
    
    def total(self, cartitem:Cartitems):
        return cartitem.quantity * cartitem.product.price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')
    
    class Meta:
        model = Cart
        fields = [
            'url',
            "id",
                #   'created',
                   "items", 
                   "grand_total"
                   ]
        read_only_fields = ['id']
        
    
    
    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([ item.quantity   * item.product.price for item in items])
        return total

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem 
        fields = ["id", "product", "quantity"]
  

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order 
        fields = ['id', "placed_at", "pending_status", "owner", "items"]
        

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = ["pending_status"]


class CreateOrderSerializer(serializers.Serializer):

    cart_id = serializers.UUIDField()
    
    
    
    # def validate_cart_id(self, cart_id):
    #     if not Cart.objects.filter(pk=cart_id).exists():
    #         raise serializers.ValidationError("This cart_id is invalid")
        
    #     elif not Cartitems.objects.filter(cart_id=cart_id).exists():
    #         raise serializers.ValidationError("Sorry your cart is empty")
        
    #     return cart_id
    
    
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(owner_id = user_id)
            cartitems = Cartitems.objects.filter(cart_id=cart_id)
            orderitems = [
                OrderItem(order=order, 
                    product=item.product, 
                    quantity=item.quantity
                    )
            for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            Cart.objects.filter(id=cart_id).delete()
            return order
