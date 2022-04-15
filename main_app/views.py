from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog
from .models import Comment
from .forms import BlogForm
from .forms import CommentForm

# Create your views here

def home(request):
    return render(request, 'home.html')

def explore(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'explore_list.html', {'blogs': blogs})

@login_required(login_url='/login/')
def blogs(request):
    blogs = Blog.objects.filter(user_id=request.user.id).order_by('-created_at')
    return render(request, 'blogs_list.html', {'blogs': blogs})

# @login_required(login_url='/login/')
def single_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    comments = Comment.objects.all().order_by('id')
    new_comment = None
    # def get_context_data(self, **kwargs):
    #     data = super(single_blog, self).get_context_data(**kwargs)
    #     likes_connected = get_object_or_404(Blog, id=self.kwargs['pk'])
    #     liked = False
    #     if likes_connected.likes.filter(id=self.request.user.id).exists():
    #         liked = True
    #     data['number_of_likes'] = likes_connected.number_of_likes()
    #     data['blog_is_liked'] = liked
    #     return data
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog_post.html', {'blog': blog, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

@login_required(login_url='/login/')
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            blog = form.save()
            return redirect('blogs')
    else:
        form = BlogForm()
    context = {'form': form, 'header': 'Add New Blog', 'user': request.user}
    return render(request, 'create_blog.html', context)

@login_required(login_url='/login/')
def edit_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save()
            return redirect('blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'edit_blog.html', {'form': form})

@login_required(login_url='/login/')
def delete_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    if blog.user_id == request.user.id:
        blog.delete()
    print(blog, request.user, 'REQUEST')
    return redirect('blogs')

def login_page(request):
    return render(request, 'login.html')

def welcome(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return redirect('blogs')
    else:
        return HttpResponse('<h1>Something went wrong with login</h1>')
        # print('Something went wrong with login')
        # return render(request, 'login.html')

def profile_page(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('blogs')
        else:
            messages.success(request, "Registration unsuccessful." )
            return redirect('signup')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login/')
def delete_comment(request, pk, comment_pk):
    comment = Comment.objects.get(blog_id=pk, id=comment_pk)
    if comment.user_id == request.user.id:
        comment.delete()
    # print(comment, request.user, 'REQUEST')
    return redirect(f'/blogs/{pk}')

@login_required(login_url='/login/')
def edit_comment(request, pk, comment_pk):
    comment = Comment.objects.get(blog_id=pk, id=comment_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect(f'/blogs/{pk}')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'comment_form': form})

# @login_required(login_url='/login/')
# def like(request, pk):
#     blog = get_object_or_404(Blog, id=request.POST.get('blog_id'))
#     if blog.likes.filter(id=request.user.id).exists():
#         blog.likes.remove(request.user)
#     else:
#         blog.likes.add(request.user)
#     # blog.likes.add(request.user)
#     return HttpResponseRedirect(reverse('like_blog', args=[str(pk)]))