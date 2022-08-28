import uuid
from django.db import models
from users.models import User
from django.utils.translation import gettext as _


class Profile(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User,
                                related_name="profile",
                                on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    is_author = False

    # date and time data
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # additional :
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.username
