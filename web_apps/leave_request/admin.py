from django.contrib import admin

from leave_request.models import LeaveBalance, LeaveDetail, LeaveRequest


# Register your models here.
admin.site.register(LeaveRequest)
admin.site.register(LeaveBalance)
admin.site.register(LeaveDetail)
