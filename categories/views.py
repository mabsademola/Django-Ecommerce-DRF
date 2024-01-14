from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

class ApiCat(APIView):
   def get(self, request,pk):
      product = get_object_or_404(Category, title=pk)
      serializer_class = CategorySerializer(product,context={"request": request})
      return Response(serializer_class.data, status=status.HTTP_200_OK)
