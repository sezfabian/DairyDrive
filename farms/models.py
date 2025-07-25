from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
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
    max_users = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ExpenseCategory(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text='Hex color code (e.g., #3B82F6)')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.farm.name}"

    class Meta:
        ordering = ['name']
        unique_together = ['farm', 'name']  # Prevent duplicate category names within the same farm
        verbose_name_plural = 'Expense Categories'


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


class EquipmentPurchase(models.Model):
    PURCHASE_STATUS = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('cheque', 'Cheque'),
        ('credit', 'Credit'),
        ('lease', 'Lease'),
        ('other', 'Other'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='equipment_purchases')
    equipment_name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    supplier_contact = models.CharField(max_length=255, blank=True, null=True)
    purchase_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    warranty_expiry = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='bank_transfer')
    payment_status = models.CharField(max_length=20, choices=PURCHASE_STATUS, default='pending')
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    transactions = models.ManyToManyField('Transaction', related_name='equipment_purchases', blank=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.equipment_name} - {self.farm.name} - {self.total_cost}"

    class Meta:
        ordering = ['-purchase_date']

    def save(self, *args, **kwargs):
        # Calculate total cost if not provided
        if not self.total_cost:
            self.total_cost = self.unit_cost * self.quantity
        super().save(*args, **kwargs)

    @property
    def total_paid(self):
        """Calculate total amount paid through transactions"""
        return self.transactions.filter(transaction_type='outgoing').aggregate(total=Sum('amount'))['total'] or 0

    @property
    def pending_amount(self):
        """Calculate pending payment amount"""
        return max(0, self.total_cost - self.total_paid)

    def update_payment_status(self):
        """Update payment status based on transactions"""
        total_paid = self.total_paid
        if total_paid >= self.total_cost:
            self.payment_status = 'paid'
            self.payment_date = timezone.now().date()
        elif total_paid > 0:
            self.payment_status = 'partial'
        elif self.due_date < timezone.now().date():
            self.payment_status = 'overdue'
        else:
            self.payment_status = 'pending'
        self.save()

    def add_transaction(self, transaction):
        """Add a transaction and update payment status"""
        self.transactions.add(transaction)
        self.update_payment_status()

    def remove_transaction(self, transaction):
        """Remove a transaction and update payment status"""
        self.transactions.remove(transaction)
        self.update_payment_status()


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
    transaction_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate transaction code if not provided
        if not self.transaction_code:
            self.transaction_code = f"TXN{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.farm.name}"

    class Meta:
        ordering = ['-transaction_date']


class Expense(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='expenses')
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount} - {self.farm.name}"

    class Meta:
        ordering = ['-due_date']

    def save(self, *args, **kwargs):
        # Update payment status based on due date
        if self.due_date < timezone.now().date():
            self.payment_status = 'overdue'
        super().save(*args, **kwargs)