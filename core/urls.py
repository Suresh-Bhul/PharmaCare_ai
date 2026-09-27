"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.payment.views import payment_callback

urlpatterns = [
    path('admin/', admin.site.urls),

    #Apps/APIs
    path('api/supplier/', include('apps.supplier.api.urls')),
    path('api/medicine/', include('apps.medicine.api.urls')),
    path('api/customer/', include('apps.customer.api.urls')),
    path('api/pharmacy/', include('apps.pharmacy.api.urls')),
    path('api/purchase/', include('apps.purchase.api.urls')),
    path('api/inventory/', include('apps.inventory.api.urls')),
    path('api/sales/', include('apps.sales.api.urls')),

    #Payment
    path('callback/', payment_callback, name="callback"),


    #Simplejwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #Swagger/APIs-Documents
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redocs/', SpectacularRedocView.as_view(url_name='schema'), name='redocs'),


    # Django-template frontend (session auth, server rendered pages)
     #Apps/CRUD Operations
    path('suppliers/', include('apps.supplier.urls')),
    path('purchases/', include('apps.purchase.urls')),

    path('patients/', include('apps.customer.urls')),
    path('medicines/', include('apps.medicine.urls')),


]


