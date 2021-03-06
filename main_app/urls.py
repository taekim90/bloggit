from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('logout/', views.logout_view, name='logout'),
    path('explore/', views.explore, name='explore'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/create', views.create_blog, name='create_blog_form'),
    path('blogs/<int:pk>/', views.single_blog, name='blog_details'),
    # path('blogs/<int:pk>/', views.like, name='blogpost_like'),
    path('blogs/<int:pk>/edit', views.edit_blog, name='edit_blog_form'),
    path('blogs/<int:pk>/delete', views.delete_blog, name='delete_blog'),
    path('blogs/<int:pk>/edit_comment/<int:comment_pk>', views.edit_comment, name='edit_comment'),
    path('blogs/<int:pk>/delete_comment/<int:comment_pk>', views.delete_comment, name='delete_comment'),
    
]