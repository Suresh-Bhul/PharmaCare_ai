from django.db import models

# Create your models here.
class CustomerGender(models.TextChoices):
    MALE = "male","Male"
    FEMALE = "female", "Female"
    OTHERS = "others", "Others"

class CustomerStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"

class Customer(models.Model):
    full_name = models.CharField(max_length=50, verbose_name="Full Name")
    phone = models.PositiveBigIntegerField(unique=True, verbose_name="Phone Number")
    email = models.EmailField(max_length=50, unique=True, verbose_name="Email Address")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=10, choices=CustomerGender.choices)
    address = models.CharField(max_length=100, verbose_name="Address")
    emergency_contact = models.PositiveBigIntegerField(null=True, blank=True,verbose_name="Emergency Contact")
    status = models.CharField(max_length=15, choices=CustomerStatus.choices, default=CustomerStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "customer"

