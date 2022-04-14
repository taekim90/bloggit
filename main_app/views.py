from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog
from .models import Comment
from .forms import BlogForm

# Create your views here

def home(request):
    return render(request, 'home.html')

def explore(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'explore_list.html', {'blogs': blogs})

# def explore_blog(request, pk):
#     blog = Blog.objects.get(pk=pk)
#     return render(request, 'explore_blog.html', {'blog': blog})

@login_required(login_url='/login/')
def blogs(request):
    blogs = Blog.objects.filter(user_id=request.user.id).order_by('-created_at')
    return render(request, 'blogs_list.html', {'blogs': blogs})

@login_required(login_url='/login/')
def single_blog(request, pk):
    blog = Blog.objects.get(pk=pk)
    comments = Comment.objects.all()
    return render(request, 'blog_post.html', {'blog': blog, 'comments': comments})

@login_required(login_url='/login/')
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        # if request.user.is_authenticated:
            # form['user'] = User.objects.get(pk=request.user.id)
        form.instance.user = request.user
        if form.is_valid():
            blog = form.save()
            return redirect('blogs')
    else:
        form = BlogForm()
    context = {'form': form, 'header': 'Add New Blog', 'user': request.user}
    return render(request, 'blog_form.html', context)

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
    return render(request, 'blog_form.html', {'form': form})

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
        return render(request, 'welcome.html')
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
            return redirect('home')
        else:
            messages.success(request, "Registration unsuccessful." )

    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})