from typing import Type

from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

from blog.models import (
    Post,
    Category,
    Comment,
)


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
    comments: CommentForeignModelSerializer = \
        CommentForeignModelSerializer(many=True)


class PostCreateModelSerializer(PostBaseModelSerializer):
    """Serializer to create a new Post instance."""

    ...


class PostUpdateModelSerializer(PostBaseModelSerializer):
    """Serializer to update a post."""

    ...
