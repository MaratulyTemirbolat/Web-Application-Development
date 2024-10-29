from typing import Type

from django.forms import ModelForm

from blog.models import Post


class AddPostModelForm(ModelForm):
    """Add Post Model Form."""

    class Meta:
        """Meta class."""

        model: Type[Post] = Post
        fields: str = "__all__"
