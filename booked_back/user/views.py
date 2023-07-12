from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .serializers import ProfileSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from community.models import *
from community.serializers import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SignupAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                'userID': openapi.Schema(type=openapi.TYPE_STRING, description="아이디"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호"),
                'nickname': openapi.Schema(type=openapi.TYPE_STRING, description="닉네임"),
                'user_mbti': openapi.Schema(type=openapi.TYPE_STRING, description="한 줄 소개"),
                'image': openapi.Schema(type=openapi.TYPE_STRING, description="프로필 사진"),
            }
        ),
        responses = {
            201: openapi.Response('회원가입 성공', ProfileSerializer),
            400: openapi.Response('회원가입 실패')
        }
    )

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            password = validated_data.get('password')
            hashed_password = make_password(password)  # 비밀번호 암호화
            validated_data['password'] = hashed_password  # 암호화된 비밀번호로 교체
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT, 
                properties={
                    'userID': openapi.Schema(type=openapi.TYPE_STRING, description="아이디"),
                    'password': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호")
                }
            ),
            responses = {
                200: openapi.Response('로그인 성공', ProfileSerializer),
                401: openapi.Response('로그인 실패')
            }
        )
    
    def post(self, request):
        userID = request.data.get('userID')
        password = request.data.get('password')
        user = authenticate(request, username=userID, password=password)
        if user:
            login(request, user)
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutAPIView(APIView):
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('로그아웃 성공')
            }
        )
    
    def get(self,request):
        logout(request)
        return Response({'message': 'LogoutSuccess'}, status=200)

class MypageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses = {
            200: openapi.Response('마이페이지 접속 성공', ProfileSerializer)
        }
    )

    def get(self,request):
        user = request.user
        profile = user

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=200)
    
# 내 게시글 조회
class MyPostsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('내 게시글 조회 성공', PostSerializer),
                400: openapi.Response('등록된 유저가 아니므로 내 게시글 조회 실패')
            }
        )
    
    def get(self, request,format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        my_posts = Post.objects.filter(poster=request.user)
        serializer = PostSerializer(my_posts, many=True)
        return Response(serializer.data, status=200)

# 내 댓글 조회
class MyCommentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            responses = {
                200: openapi.Response('내 댓글 조회 성공', CommentSerializer),
                400: openapi.Response('등록된 유저가 아니므로 내 댓글 조회 실패')
            }
        )
    
    def get(self, request,format=None):
        profile = request.user
        if not profile:
            return Response({'error': 'User profile not found'}, status=400)

        my_comments = Comment.objects.filter(commenter=request.user)
        serializer = CommentSerializer(my_comments, many=True)
        return Response(serializer.data, status=200)