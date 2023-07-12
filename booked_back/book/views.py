from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import BookReviewSerializer,BookRecommendationSerializer,BookSerializer
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BookReviewAPI(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('독후감 조회 성공'),
                400: openapi.Response('등록된 유저가 아니므로 독후감 조회 실패')
            }
        )
    
    def get(self, request,format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_reviews = BookReview.objects.filter(user=profile)
        serializer = BookReviewSerializer(book_reviews, many=True)
        return Response(serializer.data, status=200)

class BookReviewCreateAPI(APIView):
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT, 
                properties={
                    'review_title': openapi.Schema(type=openapi.TYPE_STRING, description="독후감 제목"),
                    'book_title': openapi.Schema(type=openapi.TYPE_STRING, description="책 제목"),
                    'genre': openapi.Schema(type=openapi.TYPE_STRING, description="장르"),
                    'author': openapi.Schema(type=openapi.TYPE_STRING, description="저자"),
                    'feeling': openapi.Schema(type=openapi.TYPE_STRING, description="기분"),
                    'ei': openapi.Schema(type=openapi.TYPE_STRING, description="E/I"),
                    'ns': openapi.Schema(type=openapi.TYPE_STRING, description="N/S"),
                    'ft': openapi.Schema(type=openapi.TYPE_STRING, description="F/T"),
                    'jp': openapi.Schema(type=openapi.TYPE_STRING, description="J/P"),
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description="독후감 내용"),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, description="읽은 날짜"),
                    'pickpage': openapi.Schema(type=openapi.TYPE_STRING, description="기억에 남는 페이지"),
                    'pickwriting': openapi.Schema(type=openapi.TYPE_STRING, description="기억에 남는 글귀"),
                }
            ),
            responses = {
                200: openapi.Response('독후감 기록 성공'),
                400: openapi.Response('파라미터 불충분으로 독후감 기록 실패')
            }
        )
    
    def post(self, request, format=None):
        profile = request.user
        data = request.data
        review_title = data.get('review_title')
        book_title = data.get('book_title')
        genres = data.get('genre')
        authors = data.get('author')
        feelings = data.get('feeling')
        eis = data.get('ei')
        nss = data.get('ns')
        fts = data.get('ft')
        jps = data.get('jp')
        contents = data.get('content')
        created_ats=data.get('created_at')
        pickpages=data.get('pickpage')
        pickwritings=data.get('pickwriting')

        if not all([review_title, book_title, genres,authors, feelings, eis, nss, fts, jps, contents,created_ats]):
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
            genre=genres,
            author=authors,
            feeling=feelings,
            ei=ei,
            ns=ns,
            ft=ft,
            jp=jp,
            content=contents,
            created_at=created_ats,
            pickpage=pickpages,
            pickwriting=pickwritings
        )

        return Response({'message': 'Book review created successfully'}, status=201)
    
   
    
    
    
class BookReviewDetailAPI(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('독후감 상세정보 조회 성공', BookReviewSerializer)
            }
        )

    # 독후감 상서젱보 불러오기
    def get(self, request,pk,format=None):

        book_reviews = BookReview.objects.filter(pk=pk)
        serializer = BookReviewSerializer(book_reviews, many=True)
        return Response(serializer.data, status=200)
    

    @swagger_auto_schema(
            responses = {
                200: openapi.Response('독후감 좋아요 클릭 성공'),
                400: openapi.Response('등록된 유저가 아니므로 독후감 좋아요 클릭 실패')
            }
        )
    
    #좋아요
    def post(self, request, pk, format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_review = get_object_or_404(BookReview, pk=pk)
        book_review.toggle_like(profile)

        return Response({'message': 'Current Like: '+str(book_review.like.count())}, status=200)
        
class BookReviewUpdateAPI(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('독후감 조회 성공'),
                400: openapi.Response('작성한 유저가 아니므로 독후감 조회 실패')
            }
        )
    
    # 수정할 독후감 불러오기
    def get(self, request,pk,format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_reviews = BookReview.objects.filter(user=profile,pk=pk)
        serializer = BookReviewSerializer(book_reviews, many=True)
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT, 
                properties={
                    'review_title': openapi.Schema(type=openapi.TYPE_STRING, description="독후감 제목"),
                    'book_title': openapi.Schema(type=openapi.TYPE_STRING, description="책 제목"),
                    'author': openapi.Schema(type=openapi.TYPE_STRING, description="저자"),
                    'genre': openapi.Schema(type=openapi.TYPE_STRING, description="장르"),
                    'feeling': openapi.Schema(type=openapi.TYPE_STRING, description="기분"),
                    'ei': openapi.Schema(type=openapi.TYPE_STRING, description="E/I"),
                    'ns': openapi.Schema(type=openapi.TYPE_STRING, description="N/S"),
                    'ft': openapi.Schema(type=openapi.TYPE_STRING, description="F/T"),
                    'jp': openapi.Schema(type=openapi.TYPE_STRING, description="J/P"),
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description="독후감 내용"),
                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, description="읽은 날짜"),
                    'pickpage': openapi.Schema(type=openapi.TYPE_STRING, description="기억에 남는 페이지"),
                    'pickwriting': openapi.Schema(type=openapi.TYPE_STRING, description="기억에 남는 글귀"),
                }
            ),
            responses = {
                200: openapi.Response('독후감 수정 성공'),
                400: openapi.Response('파라미터 불충분으로 독후감 수정 실패')
            }
        )
    
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
        authors = data.get('author')
        feelings = data.get('feeling')
        eis = data.get('ei')
        nss = data.get('ns')
        fts = data.get('ft')
        jps = data.get('jp')
        contents = data.get('content')
        created_ats=data.get('created_ats')
        pickpages=data.get('pickpage')
        pickwritings=data.get('pickwriting')


        if not all([review_title, book_title, genres, feelings, eis, nss, fts, jps, contents,created_ats]):
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
        book_review.author=authors
        book_review.feeling = feeling
        book_review.ei = ei
        book_review.ns = ns
        book_review.ft = ft
        book_review.jp = jp
        book_review.content = contents
        book_review.created_at=created_ats
        book_review.pickpage=pickpages,
        book_review.pickwriting=pickwritings
        book_review.save()

        return Response({'message': 'Book review updated successfully'}, status=200)
    

class BookReviewDeleteAPI(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('독후감 삭제 성공'),
                400: openapi.Response('작성한 유저가 아니므로 독후감 삭제 실패')
            }
        )
    
    # 독후감 삭제
    def delete(self, request, pk, format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        book_review = get_object_or_404(BookReview, pk=pk, user=profile)
        book_review.delete()

        return Response({'message': 'Book review deleted successfully'}, status=200)
        
class AllBookReview(APIView): 
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('작성한 모든 독후감 조회', BookReviewSerializer)
            }
        )
       
    def get(self,request):
        bookreview=BookReview.objects.all()
        
        bookreviewserializer=BookReviewSerializer(bookreview,many=True)
        return Response(bookreviewserializer.data,status=200)
    
    
class BookRecommendAPI(APIView):
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT, 
                properties={
                    'category': openapi.Schema(type=openapi.TYPE_STRING, description="카테고리"),
                    'field': openapi.Schema(type=openapi.TYPE_STRING, description="분야")
                }
            ),
            responses = {
                200: openapi.Response('Category-Field에 맞게 추천된 Book 정보', BookSerializer)
            }
        )

    def post(self, request):
        category = request.data.get('category')
        field = request.data.get('field')
        serializer = BookRecommendationSerializer(data={'category': category, 'field': field})
        serializer.is_valid(raise_exception=True)
        recommendations = serializer.to_representation(serializer.validated_data)
        return Response(recommendations, status=200)
    

class BookSearchAPI(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                'search': openapi.Schema(type=openapi.TYPE_STRING, description="검색어")
            }
        ),
        responses = {
            200: openapi.Response('검색어가 포함된 제목을 가진 독후감 정보 + 개수', BookReviewSerializer),
        }
    )

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
