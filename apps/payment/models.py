from django.db import models

from apps.sales.models import Sales

# Create your models here.
class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    INITIATED = "initiated", "Initiated"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    EXPIRED = "expired", "Expired"
    REFUNDED = "refunded", "Refunded"
    PAID = "paid", "Paid"

class PaymentLog(models.Model):
    sale = models.ForeignKey(Sales, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, blank=True, default="NPR")
    status = models.CharField(max_length=20, choices=PaymentStatus.choices,default=PaymentStatus.PENDING)
    pidx = models.CharField(max_length=50, blank=True)
    gateway_response = models.CharField(max_length=20, default="Khalti")
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "paymentlog"

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"