from django.contrib import admin
from django.urls import path

from blog.views import PostListView, PostDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='posts_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
