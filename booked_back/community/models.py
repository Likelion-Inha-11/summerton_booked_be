from django.db import models
from book.models import *
from user.models import *

# Create your models here.
# 커뮤니티 게시글
class Post(models.Model):
    title=models.CharField(max_length=50)
    poster=models.ForeignKey(Profile,on_delete=models.CASCADE)
    content=models.TextField
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    commenter=models.ForeignKey(Profile, on_delete=models.CASCADE)
    content=models.CharField(max_length=200) 
    