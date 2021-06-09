from typing import Collection, Optional
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=6)

    def __str__(self):
        return self.name


class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='books')
    name = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])
    genres = models.ManyToManyField(Genre, blank=True, related_name='books')
    primary_genre = models.ForeignKey(Genre, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='primary_genre_books')
    note = models.TextField(blank=True)
    similar = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name

    def validate_unique(self, exclude: Optional[Collection[str]]) -> None:
        super().validate_unique(exclude=exclude)

        if self.__class__.objects\
            .filter(user__pk=self.user.pk, name=self.name)\
            .exclude(pk=self.pk)\
            .exists():
            raise ValidationError('Name must be unique')


def get_user_for_common_graph():
    # в общем графе находятся книги первого суперюзера на деревне
    return User.objects.filter(is_superuser=True).first()