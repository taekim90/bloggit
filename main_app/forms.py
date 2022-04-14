from django import forms
from .models import Blog
from .models import Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['user', 'title', 'content']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': "user", 'type': 'hidden'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'comment']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': "user", 'type': 'hidden'}),
            # 'name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
