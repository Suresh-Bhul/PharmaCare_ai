from django.urls import path

from apps.user import views

urlpatterns = [
    path("login/", views.PharmacyLoginView.as_view(), name="login"),
    path("logout/", views.PharmacyLogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("settings/", views.account_settings, name="account_settings"),

    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/create/", views.UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]
