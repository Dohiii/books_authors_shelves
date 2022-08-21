import uuid

from django.db import models
from users.models import User
from django.utils.translation import gettext as _


class Profile(models.Model):
    SEX_MALE = 1
    SEX_FEMALE = 2
    SEX_OTHER = 3
    GENDER_CHOICES = [
        (SEX_MALE, _("Male")),
        (SEX_FEMALE, _("Female")),
        (SEX_OTHER, _("OTHER")),
    ]
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User,
                                related_name="profile",
                                on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES,
                                              null=True, blank=True)

    """
    for future:
    is_author?
    my_books:
    my_bookshelfes
    users i follow
    my followers
    """

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
