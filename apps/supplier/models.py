from django.db import models

# Create your models here.
class Supplier(models.Model):
    company_name = models.CharField(max_length=60, help_text="Enter comaney name")
    contact_person = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.PositiveBigIntegerField()
    registration_number  = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    payment_terms = models.CharField(max_length=20, null=True, blank=True)
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # modify = models.DateTimeField(auto_created= True, default=timezone.now())

    class Meta:
        db_table = "supplier"

    def __str__(self):
        return self.company_name    #--> Display field_name
