from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
from django.utils import timezone

class Farm(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    size_unit = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    image_refference = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('maintenance', 'Needs Maintenance'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    purchase_date = models.DateField(null=True, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.farm.name}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['farm', 'name']  # Prevent duplicate equipment names within the same farm

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField()
    transaction_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.transaction_date}"

    class Meta:
        ordering = ['-transaction_date']


class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('labor', 'Labor'),
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('supplies', 'Supplies'),
        ('equipment', 'Equipment'),
        ('transportation', 'Transportation'),
        ('marketing', 'Marketing'),
        ('insurance', 'Insurance'),
        ('taxes', 'Taxes'),
        ('other', 'Other'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    transactions = models.ManyToManyField(Transaction, related_name='expenses', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.amount} - {self.farm.name}"

    class Meta:
        ordering = ['-due_date']

    @property
    def total_paid(self):
        """Calculate total amount paid through transactions"""
        return self.transactions.filter(transaction_type='outgoing').aggregate(total=Sum('amount'))['total'] or 0

    @property
    def pending_amount(self):
        """Calculate pending payment amount"""
        return max(0, self.amount - self.total_paid)

    def save(self, *args, **kwargs):
        # Calculate payment status based on transactions
        total_paid = self.total_paid
        if total_paid >= self.amount:
            self.payment_status = 'paid'
            self.payment_date = timezone.now().date()
        elif total_paid > 0:
            self.payment_status = 'partial'
        elif self.due_date < timezone.now().date():
            self.payment_status = 'overdue'
        else:
            self.payment_status = 'pending'
        super().save(*args, **kwargs)

    def add_transaction(self, transaction):
        """Add a transaction and update payment status"""
        self.transactions.add(transaction)
        self.save()  # This will trigger the payment status update

    def remove_transaction(self, transaction):
        """Remove a transaction and update payment status"""
        self.transactions.remove(transaction)
        self.save()  # This will trigger the payment status update