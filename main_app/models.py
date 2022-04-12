from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):
#     email = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     username = models.CharField(max_length=50)

#     def __str__(self):
#         return self.username

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs', default=None)
    title = models.CharField(max_length=100)
    content = models.TextField()
    # image = models.BinaryField()
    # time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return self.user.username + ' - ' + self.title
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()
    # time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return self.blog.user.username + ' : ' + self.blog.title + ' - ' + self.comment
        return self.blog.title + ' - ' + self.comment

