from django.urls import path
from employee import views

app_name = "employee"

urlpatterns = [
    path("position/", views.PositionHomePage.as_view(), name="position"),
    path("position/ajax/", views.PositionAjaxDatatable.as_view(),
         name="position_ajax"),
    path("position/create/", views.PositionCreateView.as_view(),
         name="position_create"),
    path("position/update/<str:pk>/",
         views.PositionUpdateView.as_view(), name="position_update"),
    path("position/delete/<str:pk>/",
         views.PositionDeleteView.as_view(), name="position_delete"),
    path("employee/", views.EmployeeHomePage.as_view(), name="employee"),
    path("employee/ajax/", views.EmployeeAjaxDatatable.as_view(),
         name="employee_ajax"),
    path("employee/create/", views.EmployeeCreateView.as_view(),
         name="employee_create"),
    path("employee/update/<str:pk>/",
         views.EmployeeUpdateView.as_view(), name="employee_update"),
    path("employee/delete/<str:pk>/",
         views.EmployeeDeleteView.as_view(), name="employee_delete"),
    path("employee/detail/<str:pk>/",
         views.EmployeeDetailView.as_view(), name="employee_detail"),
]
