from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post,Comment
from .serializers import PostSerializer, CommentSerializer
from book.models import BookReview
from user.models import Profile
from book.serializers import BookReviewSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# 게시글 전체 조회
class AllPostAPI(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('게시글, 독후감 조회 성공', PostSerializer),
                201: openapi.Response('게시글, 독후감 조회 성공', BookReviewSerializer)
            }
        )
    
    def get(self, request):
        post = Post.objects.all()
        
        #독후감 랜덤으로 4개 가져오기
        reviews=BookReview.objects.order_by('?')[:4]
        postserializer = PostSerializer(post, many=True)
        reviewserializer=BookReviewSerializer(reviews,many=True)
        data={
            "posts":postserializer.data,
            "reviews":reviewserializer.data
        }
        return Response(data, status=200)

# 게시글 등록 (Create)
class PostCreate(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 제목"),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 내용")
            }
        ),
        responses = {
            200: openapi.Response('게시글 작성 성공', PostSerializer)
        }
    )

    def post(self,request):
        post=Post()
        
        post.title=request.data["title"]
        post.content=request.data["content"]
        post.poster=request.user
        # post.created_at=request.data["created_at"]
        post.save()
        
        postserializer=PostSerializer(post)
        return Response(postserializer.data,status=200)
    
# 게시글 조회 (Read)
class PostRead(APIView):
    @swagger_auto_schema(
        responses = {
            200: openapi.Response('게시글 조회 성공', PostSerializer)
        }
    )

    def get(self, request, pk):
        post = get_object_or_404(Post, pk = pk)
        
        postserializer = PostSerializer(post)
        return Response(postserializer.data, status=200)

# 게시글 수정 (Update)
class PostUpdate(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 제목"),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="게시글 내용")
            }
        ),
        responses = {
            200: openapi.Response('게시글 수정 성공', PostSerializer)
        }
    )

    def put(self, request, pk):
        post = get_object_or_404(Post, pk = pk)
    
        post.title = request.data["title"]
        post.content = request.data["content"]
        # post.updated_at=request.data["updated_at"]
        post.save()

        postSerializer = PostSerializer(post)
        return Response(postSerializer.data, status=200)    

# 게시글 삭제 (Delete)    
class PostDelete(APIView):
    @swagger_auto_schema(
        responses = {
            200: openapi.Response('게시글 삭제 성공')
        }
    )

    def delete(self,request, pk):
        post = get_object_or_404(Post, pk = pk)

        post.delete()
        
        return Response({'message': 'Post deleted successfully'}, status=200)


# 답글 등록 (Create)
class CommentCreate(APIView):
    def post(self,request):
        comment=Comment()

        comment.post = request.data["post"]
        comment.content = request.data["content"]
        comment.commenter = request.user
        # comment.created_at=request.data["created_at"]

        commentserializer=CommentSerializer(comment)
        return Response(commentserializer.data,status=200)
    
# 답글 조회 (Read)
class CommentRead(APIView):
    def get(self):
        comments=Comment.objects.all()
        
        commentserializer=CommentSerializer(comments,many=True)
        return Response(commentserializer.data,status=200)

# 답글 수정 (Update)
class CommentUpdate(APIView):
    def put(self, request, pk):
        comment=Comment.objects.filter(pk=pk)
    
        comment.content = request.data["content"]
        # comment.updated_at=request.data["updated_at"]
        comment.save()

        commentserializer = CommentSerializer(comment)
        return Response(commentserializer.data, status=200)
    
# 답글 삭제 (Delete)
class CommentDelete(APIView):
    def delete(self,request, pk):
        comment = Comment.objects.filter(pk=pk)

        comment.delete()
        
        return Response(status=200)
        