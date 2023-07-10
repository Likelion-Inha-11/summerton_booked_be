from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import BookReviewSerializer,BookRecommendationSerializer,BookSerializer
from django.db.models import Q



class BookReviewAPI(APIView):

    def post(self, request, format=None):
        profile = request.user
        data = request.data
        review_title = data.get('review_title')
        book_title = data.get('book_title')
        genres = data.get('genre')
        feelings = data.get('feeling')
        eis = data.get('ei')
        nss = data.get('ns')
        fts = data.get('ft')
        jps = data.get('jp')
        contents = data.get('content')
        pickpages=data.get('pickpage')
        pickwritings=data.get('pickwriting')

        if not all([review_title, book_title, genres, feelings, eis, nss, fts, jps, contents]):
            return Response({'error': 'Missing required fields'}, status=400)
        
        genre = Genre.objects.get(name=genres)
        feeling = Feeling.objects.get(name=feelings)
        ei=EI.objects.get(name=eis)
        ns=NS.objects.get(name=nss)
        ft=FT.objects.get(name=fts)
        jp=JP.objects.get(name=jps)

        book_review = BookReview.objects.create(
            user=profile,
            review_title=review_title,
            book_title=book_title,
            genre=genre,
            feeling=feeling,
            ei=ei,
            ns=ns,
            ft=ft,
            jp=jp,
            content=contents,
            pickpage=pickpages,
            pickwriting=pickwritings
        )

        return Response({'message': 'Book review created successfully'}, status=201)
    
    def get(self, request,format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_reviews = BookReview.objects.filter(user=profile)
        serializer = BookReviewSerializer(book_reviews, many=True)
        return Response(serializer.data, status=200)
    
class BookReviewDetailAPI(APIView):
    # 독후감 상서젱보 불러오기
    def get(self, request,pk,format=None):

        book_reviews = BookReview.objects.filter(pk=pk)
        serializer = BookReviewSerializer(book_reviews, many=True)
        return Response(serializer.data, status=200)
    
    #좋아요
    def post(self, request, pk, format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_review = get_object_or_404(BookReview, pk=pk)
        book_review.toggle_like(profile)

        return Response({'message': 'Current Like: '+str(book_review.like.count())}, status=200)
        
class BookReviewUDAPI(APIView):
    # 수정할 독후감 불러오기
    def get(self, request,pk,format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_reviews = BookReview.objects.filter(user=profile,pk=pk)
        serializer = BookReviewSerializer(book_reviews, many=True)
        return Response(serializer.data, status=200)
    
    # PUT 메서드 추가
    def put(self, request, pk, format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_review = get_object_or_404(BookReview, pk=pk, user=profile)

        data = request.data
        review_title = data.get('review_title')
        book_title = data.get('book_title')
        genres = data.get('genre')
        feelings = data.get('feeling')
        eis = data.get('ei')
        nss = data.get('ns')
        fts = data.get('ft')
        jps = data.get('jp')
        contents = data.get('content')

        if not all([review_title, book_title, genres, feelings, eis, nss, fts, jps, contents]):
            return Response({'error': 'Missing required fields'}, status=400)

        genre = Genre.objects.get(name=genres)
        feeling = Feeling.objects.get(name=feelings)
        ei = EI.objects.get(name=eis)
        ns = NS.objects.get(name=nss)
        ft = FT.objects.get(name=fts)
        jp = JP.objects.get(name=jps)

        book_review.review_title = review_title
        book_review.book_title = book_title
        book_review.genre = genre
        book_review.feeling = feeling
        book_review.ei = ei
        book_review.ns = ns
        book_review.ft = ft
        book_review.jp = jp
        book_review.content = contents
        book_review.save()

        return Response({'message': 'Book review updated successfully'}, status=200)
    

class BookReviewDeleteAPI(APIView):
    # 독후감 삭제
    def delete(self, request, pk, format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_review = get_object_or_404(BookReview, pk=pk, user=profile)
        book_review.delete()

        return Response({'message': 'Book review deleted successfully'}, status=200)
        
class AllBookReview(APIView):    
    def get(self,request):
        bookreview=BookReview.objects.all()
        
        bookreviewserializer=BookReviewSerializer(bookreview,many=True)
        return Response(bookreviewserializer.data,status=200)
    
    
class BookRecommendAPI(APIView):
    def post(self, request):
        category = request.data.get('category')
        field = request.data.get('field')
        serializer = BookRecommendationSerializer(data={'category': category, 'field': field})
        serializer.is_valid(raise_exception=True)
        recommendations = serializer.to_representation(serializer.validated_data)
        return Response(recommendations, status=200)
    

class BookSearchAPI(APIView):
    def post(self,request):
        search=request.data.get('search')
        #title__icontains는 Django의 쿼리셋 API에서 사용되는 필터 표현식
        #icontains: 필드에 대해 대서문자를 구분하지 않고 해당 문자열 포함된 경우 검색
        books=BookReview.objects.filter(book_title__icontains=search)
        serializer=BookReviewSerializer(books,many=True)
        total=books.count()
        data={
            "searchresult":serializer.data,
            "totalcount":total
        }
        return Response(data,status=200)        
    
        
        
    

# Create your views here.
