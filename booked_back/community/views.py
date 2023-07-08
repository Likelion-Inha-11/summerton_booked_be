from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post,Comment
from .serializers import PostSerializer, CommentSerializer
# Create your views here.

class PostAPI(APIView):
    # 게시글 등록
    def post(self,request):
        post=Post()
        
        post.title=request.data["title"]
        post.content=request.data["content"]
        post.writer=request.user
        post.save()
        
        postserializer=PostSerializer(post)
        return Response(postserializer.data,status=200)
    
    # 게시글 조회
    def get(self):
        posts=Post.objects.all()
        
        postserializer=PostSerializer(posts,many=True)
        return Response(postserializer.data,status=200)
    
    #게시글 수정
    def put(self,request):
        
        post=Post.objects.get(id=request.data[id])
    
     # 데이터 수정
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.save()

        postSerializer = PostSerializer(post)
        return Response(postSerializer.data, status=200)    
    
    # Post 삭제 (Update)
    def delete(self, request):

        # id로 Post 조회
        post = Post.objects.get(id = request.data[id])

        # 삭제
        post.delete()
        
        return Response(status=200)
                

