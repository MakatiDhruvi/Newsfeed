from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Category

class UserRegistrationFrom(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    OPTIONS = (
        ("business", "business"),
        ("entertainment", "entertainment"),
        ("general", "general"),
        ("health", "health"),
        ("science", "science"),
        ("sports", "sports"),
        ("technology", "technology"),
    )
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)
    class Meta:
        model = Profile
        fields = ['image', 'category']
