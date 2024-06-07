from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('quotes/', views.quotes, name='quotes'),
    path('authors/<int:pk>/', views.author_about, name='author_about'),
    path('authors/', views.authors, name='authors')
]
