from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False, allow_null=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.ReadOnlyField(source='following.username')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        fields = '__all__'
        model = Follow

    def to_internal_value(self, data):
        following_username = data.get('following')
        following_user = get_object_or_404(User, username=following_username)
        data['following'] = following_user.pk
        return super().to_internal_value(data)
