from branch import views
from django.urls import path

app_name = "branch"

urlpatterns = [
    path("branch/", views.BranchHomePage.as_view(), name="branch"),
    path("branch/ajax/", views.BranchAjaxDatatable.as_view(), name="branch_ajax"),
    path("branch/create/", views.BranchCreateView.as_view(), name="create"),
    path("branch/update/<str:pk>/",
         views.BranchUpdateView.as_view(), name="update"),
    path("branch/delete/<str:pk>/",
         views.BranchDeleteView.as_view(), name="delete"),
    path("headquarter/", views.HeadQuarterPage.as_view(), name="headquarter"),
    path("headquarter/ajax/", views.HeadQuarterAjaxDatatable.as_view(),
         name="headquarter_ajax"),
    path("headquarter/create/", views.HeadQuarterCreateView.as_view(),
         name="headquarter_create"),
    path("headquarter/update/<str:pk>/",
         views.HeadQuarterUpdateView.as_view(), name="headquarter_update"),
    path("headquarter/delete/<str:pk>/",
         views.HeadQuarterDeleteView.as_view(), name="headquarter_delete"),
]
