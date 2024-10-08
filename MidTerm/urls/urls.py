from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path, include

from apps.tasks.views import UserViewSet, TaskViewSet


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
    prefix="tasks/tasks",
    viewset=TaskViewSet,
    basename="task"
)

urlpatterns += [
    path("api/v1/", include(router.urls)),
]