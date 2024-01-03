# yourappname/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Post,ChatMessage

class YourProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'profile_photo']


class CustomUserCreationForm(UserCreationForm):
    profile_photo = forms.ImageField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'bio', 'profile_photo']

    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo')
        if not profile_photo:
            raise forms.ValidationError('Profile photo is required.')
        return profile_photo

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {'content': forms.Textarea(attrs={'required': True})}


# Add this to your forms.py
class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
