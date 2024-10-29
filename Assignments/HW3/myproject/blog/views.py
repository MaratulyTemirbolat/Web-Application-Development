from typing import Type, Any

from django.views.generic import ListView, DetailView
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from blog.models import Post
from blog.forms import AddPostModelForm
from blog.statuses import HTTP_OK_STATUS


class PostListView(ListView):
    template_name: str = "blog/index.html"
    model: Type[Post] = Post
    context_object_name: str = "posts"

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        searched_title: str = self.request.GET.get("s", "").lower()
        if searched_title:
            context["posts"] = Post.objects.annotate(
                lower_title=Lower("title")
            ).filter(
                lower_title__icontains=searched_title
            ).select_related(
                "author",
            ).prefetch_related(
                "categories"
            )
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


def create_post(request: WSGIRequest) -> HttpResponse:
    form: AddPostModelForm = AddPostModelForm()
    if request.method == "POST":
        form = AddPostModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Post created successfully.")
    return render(
        request=request,
        template_name="blog/post_add.html",
        context={
            "form": form
        },
        status=HTTP_OK_STATUS
    )