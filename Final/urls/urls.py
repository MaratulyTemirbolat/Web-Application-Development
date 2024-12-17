from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path, include

from apps.auths.views import UserViewSet
from apps.orders.views import ProductViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# ----------------------------------------------
# API Endpoints
#
router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix="auths/users",
    viewset=UserViewSet,
    basename="user"
)
router.register(
    prefix="orders/products",
    viewset=ProductViewSet,
    basename="product"
)

urlpatterns += [
    path("api/v1/", include(router.urls)),
]