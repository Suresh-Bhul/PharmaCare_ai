from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=10, verbose_name="Category")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"


class Dosage_form(models.TextChoices):
    TABLET = "tablet", "Tablet"
    CAPSULE = "capsule", "Capsule"
    SYRUP = "syrup", "Syrup"
    INJECTION = "injection", "Injection"
    CREAM = "cream", "Cream"
    OINTMENT = "ointment", "Ointment"
    GEL = "gel", "Gel"
    LOTION = "lotion", "Lotion"
    DROPS = "drops", "Drops"
    SPRAY = "spray", "Spray"
    INHALER = "inhaler", "Inhaler"
    POWDER = "powder", "Powder"
    GRANULES = "granules", "Granules"
    SUSPENSION = "suspension", "Suspension"
    SOLUTION = "solution", "Solution"
    EMULSION = "emulsion", "Emulsion"
    SUPPOSITORY = "suppository", "Suppository"
    PATCH = "patch", "Patch"
    LOZENGE = "lozenge", "Lozenge"
    PASTE = "paste", "Paste"
    SHAMPOO = "shampoo", "Shampoo"
    FOAM = "foam", "Foam"
    ELIXIR = "elixir", "Elixir"
    OIL = "oil", "Oil"

class MedicineStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    OUT_OF_STOCK = "out_of_stock", "Out of Stock"
    DISCONTINUED = "discontinued", "Discontinued"
    EXPIRED = "expired", "Expired"


class Medicine(models.Model):
    name = models.CharField(max_length=80, verbose_name="Medicine Name")
    generic_name = models.CharField(max_length=100, blank=True)
    brand_name = models.CharField(max_length=100, blank=True)
    medicine_code = models.IntegerField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    dosage_form = models.CharField(max_length=20, choices=Dosage_form.choices, default=Dosage_form.TABLET)
    strength = models.CharField(max_length=10, help_text="store mg/mcq/IU/mL of medicine",)
    barcode = models.PositiveIntegerField(unique=True)
    purchase_price = models.DecimalField(max_digits=10,decimal_places=2)
    selling_price = models.DecimalField(max_digits=10,decimal_places=2)
    tax_rate = models.DecimalField(max_digits=10,decimal_places=2)
    reorder_level = models.IntegerField(default=10)
    storage_location = models.CharField(max_length=150,null=True,blank=True)
    manufacture_date = models.DateField()
    status = models.CharField(max_length=15, choices=MedicineStatus.choices, default=MedicineStatus.ACTIVE)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "medicine"
        


