from django.db import models
from django.contrib.auth.models import User
from farms.models import Farm
from datetime import date

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),)

class AnimalType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AnimalBreed(models.Model):
    type = models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ArtificialInsemination(models.Model):
    STATUS_CHOICES = [
        ('SUCCESSFUL', 'Successful'),
        ('UNSUCCESSFUL', 'Unsuccessful'),
        ('PENDING', 'Pending'),
    ]

    animal = models.ForeignKey('Animal', on_delete=models.CASCADE, related_name='ai_records')
    semen_code = models.CharField(max_length=100)
    breed = models.ForeignKey(AnimalBreed, on_delete=models.CASCADE)
    insemination_date = models.DateField()
    technician = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal.name} - {self.semen_code} - {self.insemination_date}"

class Animal(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    breed = models.ForeignKey(AnimalBreed, on_delete=models.CASCADE,  null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER)
    weight = models.DecimalField(decimal_places=2,  max_digits=10, blank=True, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True, default=None)
    dam = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='offspring_dam')
    sire = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='offspring_sire')
    ai_sire = models.ForeignKey(ArtificialInsemination, on_delete=models.SET_NULL, null=True, blank=True, related_name='offspring_ai')
    date_of_purchase = models.DateField(null=True, blank=True)
    date_of_sale = models.DateField(null=True, blank=True)
    is_on_sale = models.BooleanField(default=False)
    price = models.IntegerField(null=True, blank=True)
    purchase_price = models.IntegerField(null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    to_be_archived = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        today = date.today()
        if self.date_of_birth:
            years = today.year - self.date_of_birth.year
            months = today.month - self.date_of_birth.month
            if self.date_of_birth.day >= 15:
                months -= 1
            if months < 0:
                years -= 1
                months += 12
            return years * 12 + months
        return {}

    def __str__(self):
        return f"{self.id} - {self.type} - {self.breed} - {self.name}"
    

class AnimalImage(models.Model):
    image_url = models.CharField(max_length=255)
    image_refference = models.CharField(max_length=255)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image_url