from typing import Type
import filetype

from django.contrib.auth.models import User

from rest_framework.serializers import (
    ModelSerializer,
    ImageField,
    HiddenField,
    CurrentUserDefault,
)
from blog.models import (
    Post,
    Category,
    Comment,
)


class Base64ImageField(ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        import base64
        import uuid

        import six
        from django.core.files.base import ContentFile

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')
            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except Exception:
                self.fail(key="invalid_image")

            # Generate file name of length 12:
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(decoded_file)

            data = ContentFile(
                decoded_file, name=f"{file_name}.{file_extension}"
            )

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, decoded_file):
        # Use filetype to determine the file type from the in-memory byte content
        kind = filetype.guess(decoded_file)

        if kind is None:
            return None

        # Map the kind.mime to the correct file extension
        mime_to_extension = {
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/gif': 'gif',
            'image/bmp': 'bmp',
            'image/webp': 'webp',
            'image/tiff': 'tiff',
        }

        extension = mime_to_extension.get(kind.mime)

        return extension


class UserAuthorForeignModelSerializer(ModelSerializer):
    """User as an Author serializer at cases of being a foreign key."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[User] = User
        exclude: tuple[str, str, str, str] = (
            "password",
            "username",
            "groups",
            "user_permissions",
        )
        read_only_fields: tuple[str] = (
            'id',
        )


class CategoryBaseModelSerializer(ModelSerializer):
    """Category base main serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Category] = Category
        fields: str = "__all__"
        read_only_fields: tuple[str] = (
            'id',
        )


class CategoryForeignModelSerializer(CategoryBaseModelSerializer):
    """Category serializer as a foreign key cases."""
    ...


class PostBaseModelSerializer(ModelSerializer):
    """Post base main serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Post] = Post
        fields: str = "__all__"
        read_only_fields: tuple[str] = (
            'id',
        )


class PostForeignModelSerializer(ModelSerializer):
    """Post serializer as a foreign key cases."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Post] = Post
        fields: str = "__all__"
        read_only_fields: tuple[str] = (
            'id',
        )


class PostListModelSerializer(PostBaseModelSerializer):
    """Post serializer to list items."""

    author: UserAuthorForeignModelSerializer = \
        UserAuthorForeignModelSerializer()

    class Meta:
        """Customization of the Serializer."""

        model: Type[Post] = Post
        exclude: tuple[str] = (
            "categories",
        )
        read_only_fields: tuple[str] = (
            'id',
        )


class CommentBaseModelSerializer(ModelSerializer):
    """Comment base main serializer."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Comment] = Comment
        fields: str = "__all__"
        read_only_fields: tuple[str] = (
            'id',
        )


class CommentForeignModelSerializer(CommentBaseModelSerializer):
    """Comment serializer as a foreign key cases."""

    class Meta:
        """Customization of the Serializer."""

        model: Type[Comment] = Comment
        fields: str = "__all__"
        read_only_fields: tuple[str] = (
            'id',
        )


class PostDetailModelSerializer(PostBaseModelSerializer):
    """Post serializer to view item's detailed information."""

    author: UserAuthorForeignModelSerializer = \
        UserAuthorForeignModelSerializer()
    categories: CategoryForeignModelSerializer = \
        CategoryForeignModelSerializer(many=True)


class PostCreateModelSerializer(PostBaseModelSerializer):
    """Serializer to create a new Post instance."""

    image: Base64ImageField = Base64ImageField()
    author: HiddenField = HiddenField(default=CurrentUserDefault())


class PostUpdateModelSerializer(PostBaseModelSerializer):
    """Serializer to update a post."""

    ...
