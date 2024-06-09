from django.shortcuts import render, redirect
from .models import Quote, Tag, Author
import requests
from django.core.paginator import Paginator
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm

def home(request):
    return render(request, 'quotes/home.html')

def quotes(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quotes/quotes.html', {'page_obj': page_obj})

def authors(request):
    authors_all = Author.objects.all()
    paginator = Paginator(authors_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'quotes/authors.html', {'page_obj': page_obj})

def author_about(request, author_id):
    author = Author.objects(id=author_id).first()
    author_quotes = Quote.objects.filter(author=author_id).all()
    return render(request, 'quotes/author_about.html', {'author': author, 'author_quotes': author_quotes})

def quotes_by_tag(request, tag):
    quotes = Quote.objects(tags__name=tag)
    return render(request, 'quotes/quotes_by_tag.html', {'quotes': quotes})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:home')
        else:
            return render(request, 'quotes/register.html', context={'form': form})
        
    return render(request, 'quotes/register.html', context={'form': UserRegisterForm()})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(to='quotes:home')
    else:
        form = AuthenticationForm()
    return render(request, 'quotes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(to='quotes:home')

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:home')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})