from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import Blog
from .create_blog import BlogForm


# Create your views here.
def home(request):
    return HttpResponse('<h1>Home Page</h1>')

def explore(request):
    blogs = Blog.objects.all()
    return render(request, 'explore_list.html', {'blogs': blogs})

def blog(request):
    # print('Blog Page', Blog.objects.all())
    # return HttpResponse('<h1>Blog Page</h1>')
    blogs = Blog.objects.all()
    return render(request, 'blogs_list.html', {'blogs': blogs})

def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save()
            return redirect('blogs')
    else:
        form = BlogForm()
    context = {'form': form, 'header': 'Add New Blog'}
    return render(request, 'blog_form.html', context)