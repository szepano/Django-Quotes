from django.shortcuts import render, redirect
from .models import Quote, Tag, Author
import requests
from django.core.mail import send_mail
from quotes_dir import settings
from .forms import PasswordResetForm
from django.core.paginator import Paginator
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
import secrets
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

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

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:home')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            new_password = secrets.token_urlsafe(12)
            user.set_password(new_password)
            user.save()

            token = default_token_generator.make_token(user)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri('/reset_password/confirm/{}/{}'.format(uid, token))

            subject = 'Password reset'
            message = render_to_string('quotes/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url
            })
            email_from = settings.EMAIL_HOST
            recipients = [email]
            send_mail(subject, message, email_from, recipients)

            return render(request, 'quotes/password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'quotes/password_reset_form.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                new_password = form.cleaned_data.get('new_password1')
                user = authenticate(request, username=user.username, password=new_password)
                login(request, user)
                return render(request, 'quotes/password_reset_complete.html')
            
        else:
            form = SetPasswordForm(user)
        return render(request, 'quotes/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'quotes/password_reset_invalid.html')