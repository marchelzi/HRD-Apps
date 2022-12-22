from leave_request import views
from django.urls import path

app_name = 'leave_request'

urlpatterns = [

    path('leave_request/', views.LeaveRequestHomeView.as_view(), name='leave_request'),
    path('leave_request/ajax/', views.LeaveRequestAjaxDatatable.as_view(),
         name='leave_request_ajax'),
    path('leave_request/create/', views.LeaveRequestCreateView.as_view(),
         name='leave_request_create'),
    path('leave_request/detail/<str:pk>/',
         views.LeaveRequestDetailView.as_view(), name='leave_request_detail'),
    path('leave_request/approve/<str:token>/',
         views.LeaveApproveView.as_view(), name='leave_request_approve'),
    path("leave_request/send/<str:pk>/",
         views.LeaveInfoToPIC.as_view(), name="leave_send"),

]
