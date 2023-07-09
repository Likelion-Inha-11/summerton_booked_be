from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Post

        # Post 안의 모든 정보를 json으로 변환
        fields = '__all__'
        read_only_fields = ('comment_set', 'comment_count')