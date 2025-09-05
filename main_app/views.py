from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from .models import Post, Reply, Like,Category
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'
    

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('home_page')
    template_name = 'registration/sign-up.html'

class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(post_content__icontains=query)
        return queryset

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class PostUserView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'post/post_user.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class PostDetailsView(DetailView):
    model = Post
    template_name = 'post/post_details.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/post_form.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')
    
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'post/post_details.html'
    success_url = reverse_lazy('post_list')
    pk_url_kwarg = 'post_id'

