from django.db import models
from django.contrib.auth.models import User
from farms.models import Farm
from animals.models import AnimalType, Animal
from datetime import date, datetime

class AnimalFeedType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   


    def __str__(self):
        return self.name

class AnimalFeed(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    animal_feed_type = models.ForeignKey(AnimalFeedType, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    unit = models.CharField(max_length=255, default='kg')
    cost_per_unit = models.DecimalField(decimal_places=2,  max_digits=10, default=0)
    inventory = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    animal_types = models.ManyToManyField(AnimalType)

    def __str__(self):
        return f"{self.name} - {self.farm.name} - {self.animal_feed_type.name} - {self.inventory}{self.unit}"

class AnimalFeedEntry(models.Model):
    animal_feed = models.ForeignKey(AnimalFeed, on_delete=models.CASCADE)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2,  max_digits=10, null=True, blank=True)
    feed_date = models.DateField(null=True, blank=True)
    feed_time = models.TimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, related_name="entry_deleted_by", on_delete=models.CASCADE, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.animal_feed.inventory -= self.quantity
            self.animal_feed.save()
        if self.is_deleted:
            self.animal_feed.inventory += self.quantity
            self.animal_feed.save()
            self.deleted_at = datetime.now()
        super(AnimalFeedEntry, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal_type.name} - {self.animal_feed.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class AnimalFeedPurchase(models.Model):
    animal_feed = models.ForeignKey(AnimalFeed, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2,  max_digits=10, null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, related_name="deleted_by", on_delete=models.CASCADE, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.animal_feed.cost_per_unit = ((self.animal_feed.cost_per_unit * self.animal_feed.inventory) + (self.cost * self.quantity)) / (self.animal_feed.inventory + self.quantity)
            self.animal_feed.inventory += self.quantity
            self.animal_feed.save()
        if self.is_deleted:
            self.animal_feed.inventory -= self.quantity
            self.animal_feed.save()
            self.deleted_at = datetime.now()
        super(AnimalFeedPurchase, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal_feed.name} - {self.quantity} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
