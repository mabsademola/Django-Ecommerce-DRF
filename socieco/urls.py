from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from api.routers import router,product_router,cart_router
from categories.views import ApiCat


api_urls_patterns= [
    path(r'', include(router.urls)),
    path(r'', include(product_router.urls)),
    path(r'', include(cart_router.urls)),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.jwt')),
   

    # path(r'cat/<str:pk>',ApiCat.as_view(),)
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/',include(api_urls_patterns)),
 
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)