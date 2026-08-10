from django.db import models

# Create your models here.
class District(models.Model):
    district_id = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
    

class Pharmacy(models.Model):
    name = models.CharField(max_length=150, verbose_name="Pharmacy Name")
    registration_number = models.PositiveIntegerField(max_length=50, unique=True, verbose_name="Registration Number")
    email = models.EmailField(unique=True)
    phone = models.PositiveBigIntegerField()
    website = models.URLField(blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pharmacy"
        
