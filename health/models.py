from django.db import models
from django.core.validators import MinValueValidator
from animals.models import Animal
from farms.models import Farm

class Veterinarian(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='veterinarians')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.specialization}"

    class Meta:
        ordering = ['name']

class HealthCondition(models.Model):
    SEVERITY_CHOICES = [
        ('MILD', 'Mild'),
        ('MODERATE', 'Moderate'),
        ('SEVERE', 'Severe'),
        ('CRITICAL', 'Critical'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    is_contagious = models.BooleanField(default=False)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='health_conditions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.severity})"

    class Meta:
        ordering = ['name']

class VetService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='vet_services')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.base_cost}"

    class Meta:
        ordering = ['name']

class HealthRecord(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='health_records')
    condition = models.ForeignKey(HealthCondition, on_delete=models.CASCADE)
    veterinarian = models.ForeignKey(Veterinarian, on_delete=models.CASCADE)
    diagnosis_date = models.DateField()
    symptoms = models.TextField()
    notes = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    resolution_date = models.DateField(blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    image_reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal.name} - {self.condition.name} ({self.diagnosis_date})"

    class Meta:
        ordering = ['-diagnosis_date']

class Treatment(models.Model):
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='treatments')
    service = models.ForeignKey(VetService, on_delete=models.CASCADE)
    treatment_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.health_record.animal.name} - {self.service.name} ({self.treatment_date})"

    class Meta:
        ordering = ['-treatment_date']
