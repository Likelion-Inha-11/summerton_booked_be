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
from .models import BookReview,Book,GenreCount,FillingCount,EICount,NSCount,FTCount,JPCount

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

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'
        
        
class GenreCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreCount
        fields = ['book','mention_count']

class FillingCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillingCount
        fields = ['book','mention_count']

class EICountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EICount
        fields = ['book','mention_count']

class NSCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = NSCount
        fields = ['book','mention_count']

class FTCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTCount
        fields = ['book','mention_count']

class JPCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = JPCount
        fields = ['book','mention_count']

class BookRecommendationSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=['장르', '감정', 'EI', 'NS', 'FT', 'JP'])
    field = serializers.CharField(max_length=255)

    def to_representation(self, instance):
        category = instance['category']
        field = instance['field']
        filtered_books = []

        if category == '장르':
            genre_counts = GenreCount.objects.filter(category__name=field, mention_count__gte=2)
            filtered_books = [genre_count.book for genre_count in genre_counts]
        elif category == '감정':
            feeling_counts = FillingCount.objects.filter(category__name=field, mention_count__gte=2)
            filtered_books = [feeling_count.book for feeling_count in feeling_counts]
        elif category == 'EI':
            ei_counts = EICount.objects.filter(category__name=field, mention_count__gte=2)
            filtered_books = [ei_count.book for ei_count in ei_counts]
        elif category == 'NS':
            ns_counts = NSCount.objects.filter(category__name=field, mention_count__gte=2)
            filtered_books = [ns_count.book for ns_count in ns_counts]
        elif category == 'FT':
            ft_counts = FTCount.objects.filter(category__name=field, mention_count__gte=2)
            filtered_books = [ft_count.book for ft_count in ft_counts]
        elif category == 'JP':
            jp_counts = JPCount.objects.filter(category__name=field, mention_count__gte=2)
            filtered_books = [jp_count.book for jp_count in jp_counts]

        book_serializer = BookSerializer(filtered_books, many=True)
        return book_serializer.data
    
