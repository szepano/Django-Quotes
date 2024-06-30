from django.urls import path, reverse
from . import views
from django.contrib.auth import views as django_views

app_name = 'quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('quotes/', views.quotes, name='quotes'),
    path('author_about/<str:author_id>/', views.author_about, name='author_about'),
    path('authors/', views.authors, name='authors'),
    path('quotes_by_tag/<tag>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('reset_password/', views.password_reset_request, name='password_reset'),
    path('reset_password/confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm')
]
