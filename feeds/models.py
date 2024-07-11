from django.db import models
from django.contrib.auth.models import User
from farms.models import Farm
from animals.models import AnimalType, Animal
from datetime import date

class AnimalFeedType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class AnimalFeed(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    animal_feed_type = models.ForeignKey(AnimalFeedType, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    unit = models.CharField(max_length=255)
    cost_per_unit = models.DecimalField(null=True, blank=True)
    inventory = models.DecimalField(null=True, blank=True)
    animal_types = models.ManyToManyField(AnimalType)

