from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from animals.models import Animal, AnimalType
from farms.models import Farm

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    inventory = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], default=0)
    unit = models.CharField(max_length=20)  # e.g., liters, kg, pieces
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"

class ProductionRecord(models.Model):
    RECORD_TYPES = [
        ('individual', 'Individual Animal'),
        ('group', 'Animal Type Group'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='production_records')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='production_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=True, blank=True, related_name='production_records')
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, null=True, blank=True, related_name='production_records')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.record_type == 'individual':
            self.product.inventory += self.quantity
        else:
            self.product.inventory += self.quantity
        self.product.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.record_type == 'individual':
            self.product.inventory -= self.quantity
        else:
            self.product.inventory -= self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        if self.record_type == 'individual':
            return f"{self.quantity} {self.product.unit} from {self.animal} on {self.date}"
        else:
            return f"{self.quantity} {self.product.unit} from {self.animal_type} group on {self.date}"

class Buyer(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='buyers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('credit', 'Credit'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='sales')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.BooleanField(default=False)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        self.product.inventory -= self.quantity
        self.product.save()
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.inventory += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Sale of {self.quantity} {self.product.unit} to {self.buyer} on {self.date}" 