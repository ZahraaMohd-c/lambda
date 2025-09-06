from django.urls import path
from . import views
from .root_redirect import root_redirect


urlpatterns = [
    path('', root_redirect, name='root_redirect'),
    path('auth/signup/', views.SignUpView.as_view(), name ='signup'),

    path('home/', views.HomePageView.as_view(), name='home_page' ),

    path('posts/',views.PostListView.as_view(), name='post_list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:post_id>', views.PostDetailsView.as_view(),name='post_details'),
    path('posts/<str:username>', views.PostUserView.as_view(), name='post_user'),
    path('posts/<int:post_id>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:post_id>/delete', views.PostDeleteView.as_view(), name='post_delete'),

    path('posts/<int:post_id>/replies/new/', views.ReplyCreateview.as_view(), name='reply_create'),
    path('posts/<int:post_id>/replies/', views.ReplyListView.as_view(), name='post_replies'),
    path('replies/<int:reply_id>/', views.ReplyDetailsView.as_view(), name='reply_details'),
    path('replies/<int:reply_id>/delete', views.ReplyDeleteView.as_view(), name='reply_delete'),
    path('replies/<int:reply_id>/like/', views.toggle_like.as_view(), name='like_reply'),

]
