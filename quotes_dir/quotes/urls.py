from django.urls import path, reverse
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('quotes/', views.quotes, name='quotes'),
    path('author_about/<str:author_id>/', views.author_about, name='author_about'),
    path('authors/', views.authors, name='authors'),
    path('quotes_by_tag/<tag>/', views.quotes_by_tag, name='quotes_by_tag')
]
