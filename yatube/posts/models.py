from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model() 

class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.TextField()
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.title

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE, 
        related_name='posts'
        )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='groups',
        )
