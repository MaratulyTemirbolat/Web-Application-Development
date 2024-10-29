from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from blog.views import (
    PostListView,
    PostDetailView,
    create_post,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='posts_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/add/', create_post, name='add_post'),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
