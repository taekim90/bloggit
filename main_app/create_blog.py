from django import forms
from .models import Blog

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['user', 'title', 'content']

# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', )