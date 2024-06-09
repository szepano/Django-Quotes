from django.shortcuts import render
from .models import Quote, Tag, Author
import requests
from django.core.paginator import Paginator
# Create your views here.

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