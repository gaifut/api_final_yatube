from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


from posts.models import Comment, Follow, Group, Post
from .permissions import IsCommentAuthorOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly
    )

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('following',)

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)

        search_param = self.request.query_params.get('search', None)
        if search_param:
            return queryset.filter(following__username__icontains=search_param)
        return queryset

    def create(self, request, *args, **kwargs):
        following_username = request.data.get('following')
        user = request.user

        try:
            following_user = User.objects.get(username=following_username)
        except User.DoesNotExist:
            return Response({
                'error': f'Пользователь с именем "{following_username}"'
                'не найден'}, status=HTTPStatus.BAD_REQUEST
            )
        if user == following_user:
            return Response({
                "error": "Вы не можете подписаться сами на себя"
            }, status=HTTPStatus.BAD_REQUEST
            )

        if Follow.objects.filter(user=user, following=following_user).exists():
            return Response({
                "error": "Вы уже подписаны на этого пользователя"
            }, status=HTTPStatus.BAD_REQUEST
            )

        follow_instance = Follow.objects.create(
            user=user, following=following_user
        )
        serializer = self.get_serializer(follow_instance)
        return Response(serializer.data, status=HTTPStatus.CREATED)
