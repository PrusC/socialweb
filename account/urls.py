from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import views

app_name = 'account'

urlpatterns = [
        path('', views.main_page, name='main_page'),
        path('profile/', views.profile, name='profile'),
]
