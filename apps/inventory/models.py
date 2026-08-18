from django.db import models

# Create your models here.
class TransactionType(models.TextChoices):
    PURCHASE = "PURCHASE", "Purchase"
    SALE = "SALE", "Sale"
    SALE_RETURN = "SALE_RETURN", "Sale Return"
    PURCHASE_RETURN = "PURCHASE_RETURN", "Purchase Return"
    DAMAGE = "DAMAGE", "Damage"
    EXPIRY = "EXPIRY", "Expiry"
    MANUAL_ADJUSTMENT = "MANUAL_ADJUSTMENT", "Manual Adjustment"
    STOCK_TRANSFER = "STOCK_TRANSFER", "Stock Transfer"


class InventoryTxn(models.Model):
    batch = models.ForeignKey('medicine.MedicineBatch', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=30, choices=TransactionType.choices)
    quantity = models.PositiveIntegerField()
    reference_id = models.CharField(max_length=20, null=True, blank=True)
    previous_stock = models.PositiveIntegerField()
    new_stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_txn"

    def __str__(self):
        return self.transaction_type
    

