from datetime import timedelta
import datetime
import uuid
from django.db import models
from django.urls import reverse
from django.core.signing import Signer
from django.utils import timezone
from django.db.models import Sum

# Create your models here.


LEAVE_TYPES = (
    (0, 'Cuti Tahunan'),
)

APPROVER_STATUS = (
    (0, 'Menunggu Persetujuan'),
    (1, 'Disetujui'),
    (2, 'Ditolak'),
    (3, 'Dibatalkan'),
)


class LeaveRequest(models.Model):
    APPROVER_STATUS = APPROVER_STATUS
    WAITING_FOR_APPROVAL = APPROVER_STATUS[0][0]
    APPROVED = APPROVER_STATUS[1][0]
    REJECTED = APPROVER_STATUS[2][0]
    CANCELED = APPROVER_STATUS[3][0]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employee = models.ForeignKey(
        'employee.Employee', on_delete=models.CASCADE, related_name='leave_requests')
    status = models.IntegerField(
        choices=APPROVER_STATUS, default=WAITING_FOR_APPROVAL)
    approved_by = models.ForeignKey('employee.Employee', on_delete=models.CASCADE,
                                    related_name='approved_leave_requests',
                                    null=True,
                                    blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_detail_url(self):
        return reverse('leave_request:leave_request_detail', kwargs={'pk': self.pk})

    def get_approve_url(self, status):
        signer = Signer()
        expired_in = timezone.now() + timedelta(days=1)
        data = {
            'pk': str(self.pk),
            'status': status,
            'expired_in': expired_in.timestamp(),
            'pic': str(self.employee.branch.person_in_charge.pk),

        }
        return f'/leave_request/approve/{signer.sign_object(data)}'

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.employee} - {self.get_status_display()} - {self.created_at}'


class LeaveDetail(models.Model):
    LEAVE_TYPES = LEAVE_TYPES
    ANNUAL_LEAVE = LEAVE_TYPES[0][0]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    leave_request = models.OneToOneField(
        'leave_request.LeaveRequest',
        on_delete=models.CASCADE,
        related_name='leave_details'
    )

    leave_type = models.IntegerField(choices=LEAVE_TYPES, default=ANNUAL_LEAVE)

    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.TextField()
    duration = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.leave_request} - {self.start_date} - {self.end_date}'


class LeaveBalance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employee = models.OneToOneField(
        'employee.Employee',
        on_delete=models.CASCADE,
        related_name='leave_balances')

    total_balance = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def recalculate_balance(self):
        dt_now = datetime.datetime.now()
        total_approved_this_year = LeaveRequest.objects.filter(
            status=LeaveRequest.APPROVED,
            employee=self.employee).filter(
            created_at__year=dt_now.year).aggregate(
                Sum('leave_details__duration'))['leave_details__duration__sum']
        if total_approved_this_year is None:
            total_approved_this_year = 0
        self.balance = self.total_balance - total_approved_this_year
        self.save()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.employee} - {self.balance}'
