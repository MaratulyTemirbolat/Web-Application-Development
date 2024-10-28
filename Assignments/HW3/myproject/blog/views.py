from typing import Type, Any

from django.views.generic import ListView, DetailView

from blog.models import Post


class PostListView(ListView):
    template_name: str = "blog/index.html"
    model: Type[Post] = Post
    context_object_name: str = "posts"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "Blog Posts"
        return context


class PostDetailView(DetailView):
    template_name: str = "blog/post_detail.html"
    model: Type[Post] = Post
    context_object_name: str = "post"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context
