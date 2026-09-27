from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.user.forms import (
    ProfileForm,
    StaffUserCreationForm,
    StaffUserUpdateForm,
    StyledAuthenticationForm,
    StyledPasswordChangeForm,
)


class PharmacyLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {form.get_user().get_full_name() or form.get_user().username}!")
        return super().form_valid(form)


class PharmacyLogoutView(LogoutView):
    next_page = reverse_lazy("login")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def account_settings(request):
    if request.method == "POST":
        form = StyledPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("account_settings")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = StyledPasswordChangeForm(user=request.user)
    return render(request, "accounts/settings.html", {"form": form})


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    paginate_by = 15

    def get_queryset(self):
        qs = User.objects.all().order_by("username")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(username__icontains=q)
        return qs


class UserCreateView(CreateView):
    model = User
    form_class = StaffUserCreationForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(self.request, "User account created successfully.")
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = StaffUserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(self.request, "User account updated successfully.")
        return super().form_valid(form)


class UserDeleteView(DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user_list")

    def form_valid(self, form):
        messages.success(self.request, "User account deleted.")
        return super().form_valid(form)
