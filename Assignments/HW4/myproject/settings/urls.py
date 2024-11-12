from debug_toolbar.toolbar import debug_toolbar_urls

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from blog.views import PostViewSet


router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix="blog/posts",
    viewset=PostViewSet,
    basename="posts"
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include(router.urls)),
] + debug_toolbar_urls()
