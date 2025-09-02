from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from .models import Post, Reply, Like,Category
from django.contrib.auth.models import User # this is the user model we use to log in
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'
    

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
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
