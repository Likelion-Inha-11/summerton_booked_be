"""
URL configuration for booked_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from user.views import *
from book.views import *
from community.views import *
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title = "Booked Swagger",
        default_version = "v1",
        description = "Swagger를 사용한 'Booked' API 문서입니다",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mypage/', MypageAPIView.as_view(), name='mypage'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('mypage/posts/', MyPostsAPIView.as_view(), name='myposts'),
    path('mypage/comments/', MyCommentsAPIView.as_view(), name='mycomments'),

    path('bookreviewall/',AllBookReview.as_view(),name='all_book_review'),
    path('bookreview/',BookReviewAPI.as_view(),name='review_my_api'),
    path('bookreview/<int:pk>/',BookReviewDetailAPI.as_view(),name='review_detail_api'),
    path('bookreview/modify/<int:pk>/',BookReviewUpdateAPI.as_view(),name='review_modify_api'),
    path('bookreview/delete/<int:pk>/',BookReviewDeleteAPI.as_view(),name='review_delete_api'),
    path('bookreview/create/',BookReviewCreateAPI.as_view(),name='review_create_api'),
    path('bookrecommend/',BookRecommendAPI.as_view(),name='book_recommend_api'),
    path('bookrecommend/search/',BookSearchAPI.as_view(),name='book_search_api'),
    
    path('posts/', AllPostAPI.as_view(), name='post_api'),
    path('posts/create/', PostCreate.as_view(), name='post_create_api'),
    path('posts/<int:pk>/', PostRead.as_view(), name='post_detail_api'),
    path('posts/<int:pk>/update/', PostUpdate.as_view(), name='post_update_api'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete_api'),
    #path('login/', Login.as_view()),

    #path('login/', Login.as_view()),

    # Swagger url
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
#urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
