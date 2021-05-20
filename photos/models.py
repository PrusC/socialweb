from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from likes.models import Like
from django.contrib.contenttypes.fields import GenericRelation

USER_MODEL = get_user_model()


class Photo(models.Model):
    image = models.ImageField(upload_to='path/to/img')
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)
    
    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("photo_detail", kwargs={"pk": self.pk})

    @property
    def likes_number(self):
        return self.likes.count()

    @staticmethod
    def get_photos_by_user(user):
        return Photo.objects.filter(user=user).order_by('-date_posted')
    

class Comment(models.Model):
    post = models.ForeignKey(Photo, related_name='details', on_delete=models.CASCADE)
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)
