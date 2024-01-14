from rest_framework import viewsets,filters, status

from products.tests import initiate_payment
from . models import *
from api.filters import ProductFilter
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin,CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ProductsViewSet(viewsets.ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends= [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    ordering_fields = ['price']
    filterset_class= ProductFilter
    search_fields =['name', 'description']
    pagination_class = PageNumberPagination
 

class ReviewViewSet(viewsets.ModelViewSet):
    queryset =Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    
    def get_queryset(self):
         return Review.objects.filter(product_id=self.kwargs["product_pk"])


class ProductImageViewSet(
  
    # CreateModelMixin,
    RetrieveModelMixin,
    # ListModelMixin,
    # DestroyModelMixin, 
    viewsets.GenericViewSet
    ):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    
    def get_queryset(self):
         return ProductImage.objects.filter(product_id=self.kwargs["product_pk"])


    

class CartViewSet(
  
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin, 
    viewsets.GenericViewSet
    ):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Cart deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    








class CartItemViewSet(viewsets.ModelViewSet):
    # queryset = Cartitems.objects.all()
    # serializer_class= CartItemSerializer

    
    http_method_names = ["get", "post", "patch", "delete"]
    
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs["cart_pk"])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
          return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}
    



class OrderViewSet(viewsets.ModelViewSet):
    # queryset = Order.objects.all()
    serializer_class= OrderSerializer
    permission_classes=[IsAuthenticated]

    
    # http_method_names = ["get", "patch", "post", "delete", "options", "head"]
    
    
    @action(detail=True, methods=['POST'])
    def pay(self, request, pk):
        order = self.get_object()
        amount = order.total_price
        email = request.user.email
        order_id = str(order.id)
        # redirect_url = "http://127.0.0.1:8000/confirm"
        return initiate_payment(amount, email, order_id)
    
    # @action(detail=False, methods=["POST"])
    # def confirm_payment(self, request):
    #     order_id = request.GET.get("o_id")
    #     order = Order.objects.get(id=order_id)
    #     order.pending_status = "C"
    #     order.save()
    #     serializer = OrderSerializer(order)
        
    #     data = {
    #         "msg": "payment was successful",
    #         "data": serializer.data
    #     }
    #     return Response(data)
    
    
    # def get_permissions(self):
    #     if self.request.method in ["PATCH", "DELETE"]:
    #         return [IsAdminUser()]
    #     return [IsAuthenticated()]
            
    
    
    # def create(self, request, *args, **kwargs):
    #     serializer = CreateOrderSerializer(data=request.data, context={"user_id": self.request.user.id})
    #     serializer.is_valid(raise_exception=True)
    #     order = serializer.save()
    #     serializer = OrderSerializer(order)
    #     return Response(serializer.data)
        
    

    
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
       
    
    def get_queryset(self):
        user = self.request.user
        # if user.is_staff:
        #     return Order.objects.all()
        return Order.objects.filter(owner=user)
    
    def get_serializer_context(self):
        return {"user_id": self.request.user.id}
            
        

