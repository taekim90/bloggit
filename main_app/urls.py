from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('blogs/', views.blog, name='blogs'),
    path('blogs/create', views.create_blog, name='create_blog_form')
]