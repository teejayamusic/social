# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django import forms


















class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='related_friends')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.username
    def get_friends(self):
        friends_from = self.friendship_from.filter(is_accepted=True).values_list('to_user', flat=True)
        friends_to = self.friendship_to.filter(is_accepted=True).values_list('from_user', flat=True)
        friend_ids = set(friends_from) | set(friends_to)
        return CustomUser.objects.filter(id__in=friend_ids)

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'profile_photo']

    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo')
        if not profile_photo:
            raise forms.ValidationError('Profile photo is required.')
        return profile_photo

class Friendship(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='friendship_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='friendship_to', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        self.is_accepted = True
        self.save()

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'


User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')







# Add this to your models.py
class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} - {self.timestamp}'
