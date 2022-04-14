from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['user', 'title', 'content']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': "user", 'type': 'hidden'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
