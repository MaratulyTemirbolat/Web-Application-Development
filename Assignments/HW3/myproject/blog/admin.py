from django.contrib.admin import (
    ModelAdmin,
    register,
)

from blog.models import (
    Post,
    Comment,
    Category,
)


@register(Post)
class PostAdmin(ModelAdmin):
    ...


@register(Comment)
class CommentAdmin(ModelAdmin):
    ...


@register(Category)
class CategoryAdmin(ModelAdmin):
    ...
