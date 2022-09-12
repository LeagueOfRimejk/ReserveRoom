from django.db import models

import datetime


# Create your models here.


class Room(models.Model):
    # available = [
    #     (True, 'Dostepny'),
    #     (False, 'Niedostepny'),
    # ]

    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    available_projector = models.BooleanField(default=True)


class Reservation(models.Model):

    date = models.DateField()
    comment = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['date', 'room']


