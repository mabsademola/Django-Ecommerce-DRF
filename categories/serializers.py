from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(read_only=True,many=True,view_name='product-detail')
    class Meta:
        model = Category
        fields = ['url','category_id','title','products']
        read_only_fields = ['category_id']


class CategorySerializer1(serializers.ModelSerializer):
    # products = serializers.HyperlinkedRelatedField(read_only=True,many=True,view_name='product-detail')
    class Meta:
        model = Category
        fields = ['url','category_id','title',]
        read_only_fields = ['category_id']