from django.contrib import admin
from . import models


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'description']

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'comment']