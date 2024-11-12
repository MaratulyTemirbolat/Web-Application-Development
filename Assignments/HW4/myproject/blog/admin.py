from django.contrib.admin import register, ModelAdmin

from blog.models import Post, Category, Comment


@register(Post)
class PostAdmin(ModelAdmin):
    ...


@register(Category)
class CategoryAdmin(ModelAdmin):
    ...


@register(Comment)
class CommentAdmin(ModelAdmin):
    ...
