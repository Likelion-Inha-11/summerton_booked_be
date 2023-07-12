from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('userID', 'password', 'nickname', 'user_mbti','image')
        
        def __str__(self):
            return self.nickname
