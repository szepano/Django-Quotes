from .models import Author, Tag, Quote
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('No user with given email')
        return email

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100)
    born = forms.CharField()
    born_in = forms.CharField(max_length=100)
    desc = forms.CharField(widget=forms.Textarea)

    def save(self):
        data = self.cleaned_data
        author = Author(
            name=data['name'],
            born=data['born'],
            born_in=data['born_in'],
            desc=data['desc']
        )
        author.save()
        return author
    
class TagForm(forms.Form):
    name = forms.CharField()

class QuoteForm(forms.Form):
    quote = forms.CharField()
    tags = forms.CharField(help_text='enter tags separated by commas (",")')
    author = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['author'].choices = [(str(author.id), author.name) for author in Author.objects.all()]

    def save(self):
        data = self.cleaned_data
        quote = data['quote']
        tags = [Tag(name=i.strip()) for i in data['tags'].split(',')]
        author_id = data['author']
        author = Author.objects.get(id=author_id)

        new_quote = Quote(
            quote=f'"{quote}"',
            tags=tags,
            author=author,
        )
        new_quote.save()
        return new_quote