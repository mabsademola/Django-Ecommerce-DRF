from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id','created_at','last_update')
    list_display = ('name', 'category','price')
    search_fields = ('name',)
   

class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    # prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Cart,CartAdmin)
admin.site.register(Cartitems)
admin.site.register(Order)
admin.site.register(OrderItem)
