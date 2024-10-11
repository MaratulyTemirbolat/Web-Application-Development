from typing import Optional

from django.db.models import (
    Model,
    CharField,
    SlugField,
    TextField,
    ForeignKey,
    ManyToManyField,
    DateTimeField,
    BooleanField,
    URLField,
    EmailField,
    OneToOneField,
    CASCADE
)
from django.contrib.auth.models import User


# Author model - Represents an author, which extends the User model.
class Author(Model):
    """
    Represents an author of blog posts. This model extends the default Django User model
    and adds additional information like bio and social media URL.
    """
    
    user: User = OneToOneField(
        to=User,
        on_delete=CASCADE
    )  # Link to Django's User model
    bio: Optional[str] = TextField(
        blank=True,
        null=True
    )  # Optional bio of the author
    social_media_url: Optional[str] = URLField(
        blank=True,
        null=True
    )  # Optional social media link

    def __str__(self) -> str:
        """
        Returns a string representation of the Author, displaying the associated user's username.
        """
        return self.user.username


# Category model - Represents a category for blog posts (e.g., "Technology").
class Category(Model):
    """
    Represents a category to which blog posts can be assigned. Categories help in organizing posts.
    """
    
    # Constants
    MAX_LENGTH_NAME: int = 100  # Maximum length for category name
    MAX_LENGTH_SLUG: int = 100  # Maximum length for URL slug
    
    name: str = CharField(max_length=MAX_LENGTH_NAME, unique=True)  # Category name (must be unique)
    slug: str = SlugField(max_length=MAX_LENGTH_SLUG, unique=True)  # Slug for URL-friendly names

    def __str__(self) -> str:
        """
        Returns a string representation of the Category, displaying its name.
        """
        return self.name


# Tag model - Used for tagging blog posts with relevant keywords.
class Tag(Model):
    """
    Represents a tag that can be assigned to blog posts. Tags are useful for adding keywords to posts.
    """
    
    # Constants
    MAX_LENGTH_NAME: int = 50  # Maximum length for tag name
    MAX_LENGTH_SLUG: int = 50  # Maximum length for URL slug
    
    name: str = CharField(max_length=MAX_LENGTH_NAME, unique=True)  # Tag name (must be unique)
    slug: str = SlugField(max_length=MAX_LENGTH_SLUG, unique=True)  # URL-friendly slug for the tag

    def __str__(self) -> str:
        """
        Returns a string representation of the Tag, displaying its name.
        """
        return self.name


# Blog Post model - Represents an individual blog post.
class Post(Model):
    """
    Represents an individual blog post. Contains the main content of the post, its title, author,
    categories, tags, and timestamps.
    """
    
    # Constants
    MAX_LENGTH_TITLE: int = 200  # Maximum length for blog post title
    
    title: str = CharField(max_length=MAX_LENGTH_TITLE)  # Title of the blog post
    slug: str = SlugField(max_length=MAX_LENGTH_TITLE, unique=True)  # Unique URL slug
    author: Author = ForeignKey(Author, on_delete=CASCADE)  # ForeignKey link to the Author model
    content: str = TextField()  # Main content of the post
    created_at: DateTimeField = DateTimeField(auto_now_add=True)  # Auto-set when the post is created
    updated_at: DateTimeField = DateTimeField(auto_now=True)  # Auto-set when the post is updated
    published_at: Optional[DateTimeField] = DateTimeField(blank=True, null=True)  # Optional publish date
    is_published: bool = BooleanField(default=False)  # Boolean to indicate if the post is published
    categories: ManyToManyField = ManyToManyField(Category, related_name='posts')  # Categories for the post
    tags: ManyToManyField = ManyToManyField(Tag, related_name='posts', blank=True)  # Tags for the post

    def __str__(self) -> str:
        """
        Returns a string representation of the Post, displaying its title.
        """
        return self.title

    class Meta:
        ordering = ['-created_at']  # Order posts by creation date in descending order


# Comment model - Represents comments left by users on blog posts.
class Comment(Model):
    """
    Represents a comment left by users on blog posts. Comments can be moderated using the 'approved' field.
    """
    
    # Constants
    MAX_LENGTH_AUTHOR_NAME: int = 100  # Maximum length for comment author name
    
    post: Post = ForeignKey(Post, related_name='comments', on_delete=CASCADE)  # ForeignKey to the related Post
    name: str = CharField(max_length=MAX_LENGTH_AUTHOR_NAME)  # Name of the comment author
    email: str = EmailField()  # Email of the comment author
    content: str = TextField()  # Comment content
    created_at: DateTimeField = DateTimeField(auto_now_add=True)  # Auto-set when the comment is created
    approved: bool = BooleanField(default=False)  # Indicates if the comment is approved by admin/moderator

    def __str__(self) -> str:
        """
        Returns a string representation of the Comment, displaying the author's name and the post title.
        """
        return f'Comment by {self.name} on {self.post.title}'

    class Meta:
        ordering = ['created_at']  # Order comments by creation date in ascending order


# Like model - Tracks users liking specific blog posts.
class Like(Model):
    """
    Represents a 'like' given by a user to a blog post. A user can only like a post once.
    """
    
    post: Post = ForeignKey(Post, related_name='likes', on_delete=CASCADE)  # ForeignKey to the related Post
    user: User = ForeignKey(User, on_delete=CASCADE)  # ForeignKey to the User who liked the post
    created_at: DateTimeField = DateTimeField(auto_now_add=True)  # Auto-set when the like is created

    class Meta:
        unique_together = ('post', 'user')  # Ensures that a user can only like a post once

    def __str__(self) -> str:
        """
        Returns a string representation of the Like, displaying the username and the post they liked.
        """
        return f'{self.user.username} liked {self.post.title}'
