from django.urls import path
from . import views

urlpatterns = [
    path('auth/signup/', views.SignUpView.as_view(), name ='signup'),
    path('home/', views.HomePageView.as_view(), name='home_page' ),
    path('posts/',views.PostListView.as_view(), name='post_list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/user', views.PostUserView.as_view(), name='post_user')
]
