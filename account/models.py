from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

USER_MODEL = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='users', blank=True)
    bio = models.CharField(max_length=255, blank=True)
    registered = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


@receiver(post_save, sender=USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, slug=slugify('id'+str(instance.pk)))


@receiver(post_save, sender=USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

