from typing import (
    Type,
    Any,
)

from django.db.models import QuerySet, Manager

from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)


from blog.models import Post, Comment
from blog.handlers import DRFResponseHandler
from blog.permissions import IsUserAuthor
from blog.decorators import (
    find_queryset_object_by_query_pk,
    validate_serializer_data,
)
from blog.serializers import (
    PostBaseModelSerializer,
    PostListModelSerializer,
    PostDetailModelSerializer,
    PostCreateModelSerializer,
    PostUpdateModelSerializer,
    CommentBaseModelSerializer,
)


class PostViewSet(DRFResponseHandler, ViewSet):
    """ViewSet class for Post related endpoints."""

    queryset: Manager = Post.objects
    serializer_class: Type[PostBaseModelSerializer] = PostBaseModelSerializer
    permission_classes: tuple[IsAuthenticated, IsUserAuthor] = (IsAuthenticated, IsUserAuthor,)

    def get_queryset(self) -> QuerySet[Post]:
        """Get all Posts queryset."""

        return self.queryset.all()
    
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle GET-endpoint to obtain a list of all posts."""
        return self.get_drf_response(
            request=request,
            data=self.queryset.select_related("author"),
            serializer_class=PostListModelSerializer,
            many=True
        )

    @find_queryset_object_by_query_pk(
        queryset=Post.objects.select_related(
            "author"
        ).prefetch_related("categories"),
        class_name=Post,
        entity_name="Post"
    )
    def retrieve(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle GET-request endpoint to view a detailed information about a single post."""
        post: Post = kwargs["object"]
        return self.get_drf_response(
            request=request,
            data=post,
            serializer_class=PostDetailModelSerializer,
        )

    @validate_serializer_data(
        serializer_class=PostCreateModelSerializer
    )
    def create(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle POST-request endpoint to create a new Post."""
        serializer: PostCreateModelSerializer = kwargs["serializer"]
        post: Post = serializer.save()
        return DRFResponse(
            data=request.data,
            status=HTTP_201_CREATED
        )

    @find_queryset_object_by_query_pk(
        queryset=Post.objects,
        class_name=Post,
        entity_name="Post"
    )
    def partial_update(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle PATCH-request to update a post partially."""

        post: Post = kwargs["object"]

        self.check_object_permissions(request=request, obj=post)

        serializer: PostUpdateModelSerializer = PostUpdateModelSerializer(
            instance=post,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return DRFResponse(data=serializer.data, status=HTTP_200_OK)

    @find_queryset_object_by_query_pk(
        queryset=Post.objects,
        class_name=Post,
        entity_name="Post"
    )
    def destroy(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle DELETE-request to remove a post from a user's list."""
        post: Post = kwargs["object"]
        self.check_object_permissions(request=request, obj=post)
        post.delete()
        return DRFResponse(status=HTTP_204_NO_CONTENT)

    @action(
        methods=("GET",),
        detail=True,
        url_name="comments",
        url_path="comments",
    )
    def get_comments(
        self,
        request: DRFRequest,
        pk: str,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle GET-request to view post's comments."""
        return self.get_drf_response(
            request=request,
            data=Comment.objects.filter(
                post_id=pk,
                post__author_id=request.user.id
            ),
            serializer_class=CommentBaseModelSerializer,
            many=True
        )

    @action(
        methods=("POST",),
        detail=True,
        url_name="add-comment",
        url_path="add-comment",
    )
    @find_queryset_object_by_query_pk(
        queryset=Post.objects,
        class_name=Post,
        entity_name="Post"
    )
    def add_comment(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[Any, Any]
    ) -> DRFResponse:
        """Handle POST-request to create a new comment for a post."""
        post: Post = kwargs["object"]
        data_copy: dict[str, Any] = request.data.copy()
        data_copy["post"] = post.id
        serializer: CommentBaseModelSerializer = CommentBaseModelSerializer(
            data=data_copy
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return DRFResponse(
            data=data_copy,
            status=HTTP_201_CREATED
        )
