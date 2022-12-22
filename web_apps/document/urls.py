from django.urls import path
from document import views

app_name = "document"

urlpatterns = [
    path("document/", views.DocumentHomePage.as_view(), name="document"),
    path("document/ajax/", views.DocumentAjaxDatatable.as_view(),
         name="document_ajax"),
    path("document/create/", views.DocumentCreateView.as_view(),
         name="document_create"),
    path("document/download/<str:pk>/",
         views.DocumentGenerator.as_view(), name="document_download"),
    path("document/update/<str:pk>/",
         views.DocumentUpdateView.as_view(), name="document_update"),
    path("document/send/<str:pk>/",
         views.DocumentInfoToPIC.as_view(), name="document_send"),
    path("document/approve/<str:token>/",
         views.DocumentApproveView.as_view(), name="document_approve"),
]
