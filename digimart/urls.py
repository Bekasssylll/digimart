"""
URL configuration for digimart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from mart.models import Cart
from mart.views import AppViewSet, AppRatingViewSet, AppCommentViewSet, CartViewSet, CartProductViewSet, \
    UserProfileViewSet, DiscountUserViewSet, DiscountViewSet

router = DefaultRouter()
router.register(r"app",AppViewSet,basename='appurl')
router.register(r"app-rating",AppRatingViewSet,basename='app-rating')
router.register(r"app-comment",AppCommentViewSet,basename='app-comment')
router.register(r"cart",CartViewSet,basename='cart')
router.register(r"cart-product",CartProductViewSet,basename='cart-product')
router.register(r"profile",UserProfileViewSet,basename='profile')
router.register(r"discount",DiscountViewSet,basename='discount')
router.register(r"discountuser",DiscountUserViewSet,basename='discountuser')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refre'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('accounts/', include('allauth.urls')),
]
