from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    commenter = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_commenter(self, obj):
        return obj.commenter.nickname
    
    def get_post(self, obj):
        return obj.post.title
        


class PostSerializer(serializers.ModelSerializer):
    comment_set=serializers.SerializerMethodField()
    #comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    poster = serializers.SerializerMethodField()

    class Meta:
        model = Post

        # Post 안의 모든 정보를 json으로 변환
        fields = '__all__'
        read_only_fields = ('comment_set', 'comment_count')
        
    def get_comment_set(self, obj):
        comments = obj.comment_set.all()
        return CommentSerializer(comments, many=True).data    
        
    def get_poster(self, obj):
        return obj.poster.nickname    