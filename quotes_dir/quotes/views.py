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