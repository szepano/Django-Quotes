from .models import Author, Tag, Quote
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = ['name', 'born', 'born_in', 'desc']

# class QuoteForm(forms.ModelForm):
#     class Meta:
#         model = Quote
#         fields = ['quote', 'tags', 'author']