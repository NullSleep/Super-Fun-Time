from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Persona(models.Model):
    creator = models.ForeignKey('auth.User')
    name = models.CharField(max_length = 200)
    hours = models.IntegerField()
    person_id = models.IntegerField()
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
