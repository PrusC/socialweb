from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

USER_MODEL = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(USER_MODEL, related_name='likes',  on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_liked = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def add_like(obj, user):
        obj_type = ContentType.objects.get_for_model(obj)
        like, _ = Like.objects.get_or_create(user, obj_type, obj.id)
        return like

    @staticmethod
    def remove_like(obj, user):
        obj_type = ContentType.objects.get_for_model(obj)
        Like.objects.filter(user, obj_type, obj.id).delete()

    @staticmethod
    def is_user_liked(obj, user):
        if not user.is_authenticated:
            return False
        obj_type = ContentType.objects.get_for_model(obj)
        return Like.objects.filter(user, obj_type, obj.id).delete().exist()

    @staticmethod
    def get_users_likes(obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return USER_MODEL.objects.filter(likes__content_type=obj_type, likes__object_id=obj.id)
