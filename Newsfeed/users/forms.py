from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Category

class user_registeration_form(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

class user_update_form(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class profile_update_form(forms.ModelForm):
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
