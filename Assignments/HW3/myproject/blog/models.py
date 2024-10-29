from typing import Optional
from datetime import date

from django.db.models import (
    Model,
    TextField,
    CharField,
    ForeignKey,
    DateField,
    ManyToManyField,
    QuerySet,
    ImageField,
    CASCADE,
)
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


class Category(Model):
    """Category database model."""

    NAME_MAX_LENGTH = 100

    name: str = CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        db_index=True,
        verbose_name="Category Name",
        help_text="Enter the category name.",
    )

    def __str__(self) -> str:
        """Return the string representation of the object."""

        return self.name

    class Meta:
        """Customization of a the table."""

        verbose_name: str = "Category"
        verbose_name_plural: str = "Categories"


class CustomPostManager(QuerySet):
    """Custom Post Manager."""

    def get_published_posts(self) -> QuerySet["Post"]:
        """
        Return the published posts.
        Here published means the published date is less than or equal to the current date.

        Returns:
            QuerySet: The published posts.
        """

        return self.filter(published_at__lte=timezone.now().date())

    def get_posts_by_author(self, author_id: int) -> QuerySet["Post"]:
        """
        Return the posts by the author.

        Args:
            author_id (int): The author id.

        Returns:
            QuerySet: The posts by the author.
        """

        return self.filter(author_id=author_id)



class Post(Model):
    """Post database model."""

    TITLE_MAX_LENGTH = 100

    title: str = CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name="Post Title",
        help_text="Enter the post title.",
    )
    content: Optional[str] = TextField(
        blank=True,
        null=True,
        verbose_name="Post Content",
        help_text="Enter the post content.",
    )
    image: Optional[str] = ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
        verbose_name="Post Image",
        help_text="Upload the post image.",
    )
    author: User = ForeignKey(
        to=User,
        on_delete=CASCADE,
        related_name="posts",
        verbose_name="Author",
        help_text="Select the author of the post.",
    )
    categories: ManyToManyField = ManyToManyField(
        to=Category,
        blank=True,
        related_name="posts",
        verbose_name="Categories",
        help_text="Select the categories of the post.",
    )
    published_at: date | str = DateField(
        verbose_name="Published At",
        help_text="Enter the published date of the post.",
    )
    objects = CustomPostManager.as_manager()

    class Meta:
        """Customization of a the table."""

        verbose_name: str = "Post"
        verbose_name_plural: str = "Posts"


    def __str__(self) -> str:
        """Return the string representation of the object."""

        return self.title

    def get_absolute_url(self) -> str:
        """Return the absolute URL of the object."""
        return reverse(
            viewname="post_detail",
            kwargs={"pk": self.id}
        )


class Comment(Model):
    """Comment database model."""

    content: str = TextField(
        verbose_name="Comment Content",
        help_text="Enter the comment content.",
    )
    post: Post = ForeignKey(
        to=Post,
        on_delete=CASCADE,
        related_name="comments",
        verbose_name="Post",
        help_text="Select the post of the comment.",
    )

    def __str__(self) -> str:
        """Return the string representation of the object."""

        return self.content[:50]

    class Meta:
        """Customization of a the table."""

        verbose_name: str = "Comment"
        verbose_name_plural: str = "Comments"
