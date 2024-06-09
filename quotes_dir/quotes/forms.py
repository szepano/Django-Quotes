from .models import Author, Tag, Quote
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    bborn = forms.CharField()
    born_in = forms.CharField(max_length=100)
    desc = forms.CharField(widget=forms.Textarea)

    def save(self):
        data = self.cleaned_data
        author = Author(
            name=data['name'],
            birth_date=data['born'],
            born_in=data['born_in'],
            description=data['desc']
        )
        author.save()
        return author

class QuoteForm(forms.Form):
    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']