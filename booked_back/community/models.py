from django.db import models
from book.models import *
from user.models import *

# Create your models here.
# 커뮤니티 게시글
class Post(models.Model):
    title=models.CharField(max_length=50)  #타이틀
    poster=models.ForeignKey(Profile, on_delete=models.CASCADE) #게시글 작성자(닉네임)
    content=models.TextField(null=True) #게시글 내용
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE) #연결된 게시글
    commenter=models.ForeignKey(Profile, on_delete=models.CASCADE) #댓글 작성자(닉네임)
    content=models.CharField(max_length=200) #댓글 내용
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content