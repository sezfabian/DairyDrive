from django.db import models
from django.core.validators import MinValueValidator
from animals.models import Animal
from farms.models import Farm, Transaction
from django.db.models import Sum

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
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    transactions = models.ManyToManyField(Transaction, related_name="treatment", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.health_record.animal.name} - {self.service.name} ({self.treatment_date})"

    class Meta:
        ordering = ['-treatment_date']

    @property
    def total_paid(self):
        """Calculate total amount paid through transactions"""
        if not self.pk:  # If the object hasn't been saved yet
            return 0
        return self.transactions.filter(transaction_type='outgoing').aggregate(total=Sum('amount'))['total'] or 0

    @property
    def pending_amount(self):
        """Calculate pending payment amount"""
        return max(0, self.cost - self.total_paid)

    def save(self, *args, **kwargs):
        # First save to get an ID
        super().save(*args, **kwargs)
        
        # Now we can safely access the transactions
        total_paid = self.total_paid
        if total_paid >= self.cost:
            self.is_paid = True
            super().save(update_fields=['is_paid'])
        else:
            self.is_paid = False
            super().save(update_fields=['is_paid'])



    def add_transaction(self, transaction):
        """Add a transaction and update payment status"""
        self.transactions.add(transaction)
        self.save()  # This will trigger the payment status update

    def remove_transaction(self, transaction):
        """Remove a transaction and update payment status"""
        self.transactions.remove(transaction)
        self.save()  # This will trigger the payment status update
