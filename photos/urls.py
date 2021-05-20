from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from . import views

app_name = 'photos'

urlpatterns = [
        path('<int:pk>', views.PhotoDetail.as_view(), name='detail'),
]
