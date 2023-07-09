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
from django.urls import path
from user.views import SignupAPIView, LoginAPIView
from community.views import PostAPI
from book.views import BookReviewAPI,AllBookReview,BookReviewUDAPI,BookReviewDeleteAPI,BookReviewDetailAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('bookreviewall/',AllBookReview.as_view(),name='all_book_review'),
    path('bookreview/',BookReviewAPI.as_view(),name='review_my_api'),
    path('bookreview/<int:pk>/',BookReviewDetailAPI.as_view(),name='review_detail_api'),
    path('bookreview/modify/<int:pk>/',BookReviewUDAPI.as_view(),name='review_modify_api'),
    path('bookreview/delete/<int:pk>/',BookReviewDeleteAPI.as_view(),name='review_delete_api'),
    path('bookreview/create/',BookReviewAPI.as_view(),name='review_create_api'),
    path('posts/', PostAPI.as_view(), name='post_api'),
    path('posts/create/', PostAPI.as_view(), name='post_create_api'),
    path('posts/<int:pk>/', PostAPI.as_view(), name='post_detail_api'),
    path('posts/<int:pk>/update/', PostAPI.as_view(), name='post_update_api'),
    path('posts/<int:pk>/delete/', PostAPI.as_view(), name='post_delete_api'),
    #path('login/', Login.as_view()),
]
