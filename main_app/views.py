from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from .models import Post, Reply, Like,Category
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, PostForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'
    

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')
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
        return queryset.order_by('-post_date')

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
        return Post.objects.filter(user=self.request.user).order_by('-post_date')

class PostDetailsView(DetailView):
    model = Post
    template_name = 'post/post_details.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies = self.object.replies.order_by('-reply_date')

        if self.request.user.is_authenticated:
            for reply in replies:
                reply.liked_by_user = reply.like_reply.filter(user=self.request.user).exists()
        else:
            for reply in replies:
                reply.liked_by_user = False

        context['replies'] = replies
        return context
    
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

class ReplyCreateview(LoginRequiredMixin,CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply/reply_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'post_id': self.kwargs['post_id']})

class ReplyListView(ListView):
    model = Reply
    template_name = 'reply/reply_list.html'
    context_object_name = 'replies'

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Reply.objects.filter(post=post).order_by('-reply_date')


class ReplyDetailsView(DetailView):
    model = Reply
    template_name = 'reply/reply_details.html'
    context_object_name = 'reply'
    pk_url_kwarg = 'reply_id'


class ReplyDeleteView(DeleteView):
    model = Reply
    template_name = 'reply/reply_details.html'
    pk_url_kwarg = 'reply_id'

    def get_success_url(self):
        post_id = self.object.post.id
        return reverse_lazy('post_details', kwargs={'post_id': post_id})

class toggle_like(LoginRequiredMixin,View):

    def like_reply(request, reply_id):
        reply = get_object_or_404(Reply, id=reply_id)
        liked = False

        like_instance = Like.objects.filter(user=request.user, reply=reply).first()
        if like_instance:
        
            like_instance.delete()
        else:
            Like.objects.create(user=request.user, reply=reply)
            liked = True

        return JsonResponse({
        'liked': liked,
        'like_count': reply.like_reply.count(),
        }) 