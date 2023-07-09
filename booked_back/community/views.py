from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post,Comment
from .serializers import PostSerializer, CommentSerializer
# Create your views here.


# 게시글 전체 조회
class AllPostAPI(APIView):
    def get(self, request):
        post = Post.objects.all()

        postserializer = PostSerializer(post, many=True)
        return Response(postserializer.data, status=200)

# 게시글 등록 (Create)
class PostCreate(APIView):
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
    def get(self, request, pk):
        post = get_object_or_404(Post, pk = pk)
        
        postserializer = PostSerializer(post)
        return Response(postserializer.data, status=200)

# 게시글 수정 (Update)
class PostUpdate(APIView):
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
    def delete(self,request, pk):
        post = get_object_or_404(Post, pk = pk)

        post.delete()
        
        return Response(status=200)


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
        