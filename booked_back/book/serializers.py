'''from rest_framework import serializers
from .models import BookReview
from user.models import Profile
from django.contrib.auth import get_user_model

User=get_user_model()


class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    #user = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    class Meta:
        model = BookReview
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = None
        if request and request.user.is_authenticated:
            user = request.user.profile
        validated_data['user'] = user
        return super().create(validated_data)'''
        
from rest_framework import serializers
from .models import BookReview

class BookReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = BookReview
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request')
        user = None
        if request and request.user.is_authenticated:
            user = request.user.profile
        validated_data['user'] = user
        instance = self.Meta.model.objects.create(**validated_data)
        return instance

