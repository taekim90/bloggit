from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Blog
from .create_blog import BlogForm
from .create_user_form import SignUpForm


# Create your views here.
# def home(request):
#     # return HttpResponse('<h1>Home Page</h1>')
#     # return render(request, point to 'home.html', pass in a context dictionary)
#     return render(request, 'home.html', {})

def home(request):
    return render(request, 'home.html')

def explore(request):
    blogs = Blog.objects.all()
    return render(request, 'explore_list.html', {'blogs': blogs})

@login_required(login_url='/login/')
def blog(request):
    # print('Blog Page', Blog.objects.all())
    # return HttpResponse('<h1>Blog Page</h1>')
    blogs = Blog.objects.filter(user_id=request.user.id)
    return render(request, 'blogs_list.html', {'blogs': blogs})

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
    # Blog.objects.get(pk=pk).delete()
    blog = Blog.objects.get(pk=pk)
    if blog.user_id == request.user.id:
        blog.delete()
    print(blog, request.user, 'REQUEST')
    return redirect('blogs')

def login_page(request):
    return render(request, 'login.html')

def profile_show(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        return render(request, 'profile.html')
    else:
        return HttpResponse('<h1>Something went wrong with login</h1>')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid:
            user = form.save()
            user = authenticate(username=user.username, password=user.password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})