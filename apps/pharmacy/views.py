from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.pharmacy.forms import PharmacyForm
from apps.pharmacy.models import Pharmacy


@login_required
def pharmacy_settings(request):
    instance = Pharmacy.objects.first()

    if request.method == "POST":
        form = PharmacyForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Pharmacy details updated successfully.")
            return redirect("pharmacy_settings")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PharmacyForm(instance=instance)

    return render(request, "pharmacy/settings.html", {"form": form, "instance": instance})
