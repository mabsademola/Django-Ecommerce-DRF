from rest_framework.routers import DefaultRouter
from categories.viewset import CategoryViewSet
from products.viewset import *
from accounts.viewset import ProfileViewSet
from rest_framework_nested import routers

router = DefaultRouter()
router.register('products',ProductsViewSet)
router.register('category',CategoryViewSet)
router.register("carts", CartViewSet)
router.register("product_images", ProductImageViewSet)
router.register('profile',ProfileViewSet)
router.register("orders", OrderViewSet, 
                basename="orders"
                )

product_router = routers.NestedDefaultRouter(router, 'products',lookup='product' )
product_router.register("reviews", ReviewViewSet, basename="product-reviews")

cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemViewSet, basename="cart-items")

