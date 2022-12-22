
from users import views
from django.urls import path


app_name = "users"

urlpatterns = [
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/logout/", views.LogoutView, name="logout"),
    path("user/", views.UserIndexView.as_view(), name="index"),
    path("user/create/", views.UserCreateView.as_view(), name="user_create"),
    path("user/update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    path("user/delete/<int:pk>/", views.UserDeleteView.as_view(), name="user_delete"),
    path("user/ajax/", views.UserAjaxDatatable.as_view(), name="user_ajax"),
    path("user/change-password/<int:pk>/",
         views.UserChangePasswordView.as_view(), name="user_change_password"),

]
