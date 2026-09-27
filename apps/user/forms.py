from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import Group, User


class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username", "autofocus": True}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )


class StaffUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False, max_length=150)
    last_name = forms.CharField(required=False, max_length=150)
    role = forms.ChoiceField(
        choices=[("staff", "Pharmacy Staff"), ("admin", "Administrator")],
        initial="staff",
    )
    is_active = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "is_active", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            if name in ("is_active",):
                field.widget.attrs["class"] = (existing + " form-check-input").strip()
            else:
                field.widget.attrs["class"] = (existing + " form-control").strip()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = self.cleaned_data.get("is_active", True)
        if self.cleaned_data.get("role") == "admin":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = True
            user.is_superuser = False
        if commit:
            user.save()
        return user


class StaffUserUpdateForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=[("staff", "Pharmacy Staff"), ("admin", "Administrator")],
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["role"].initial = "admin" if self.instance.is_superuser else "staff"
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            if name == "is_active":
                field.widget.attrs["class"] = (existing + " form-check-input").strip()
            else:
                field.widget.attrs["class"] = (existing + " form-control").strip()

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("role") == "admin":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = True
            user.is_superuser = False
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
