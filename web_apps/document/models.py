from datetime import timedelta
from django.utils import timezone
from uuid import uuid4
from django.db import models
from django.core.signing import Signer
# Create your models here.


class Document(models.Model):

    STATUS_TYPES = (
        (0, 'Canceled'),
        (1, 'Pending'),
        (2, 'Approved'),
    )
    DOCUMENT_TYPES = (
        (0, 'SPK'),
        (1, 'SP'),
    )

    CANCELED = STATUS_TYPES[0][0]
    PENDING = STATUS_TYPES[1][0]
    APPROVED = STATUS_TYPES[2][0]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    employee = models.ForeignKey(
        'employee.Employee', on_delete=models.CASCADE, related_name='documents')
    approved_by = models.ForeignKey(
        'employee.Employee', on_delete=models.CASCADE, related_name='approved_documents', null=True, blank=True)

    representation = models.CharField(max_length=255)
    description = models.TextField()
    document_type = models.IntegerField(choices=DOCUMENT_TYPES, default=0)
    status = models.IntegerField(choices=STATUS_TYPES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def serial(self):
        return Document.objects.filter(
            created_at__year=self.created_at.year,
            created_at__lt=self.created_at
        ).count() + 1

    @property
    def serial_sp(self):
        if self.document_type == 1:
            return Document.objects.filter(
                created_at__year=self.created_at.year,
                created_at__lt=self.created_at,
                document_type=1,
                employee=self.employee,
                status=2
            ).count() + 1
        raise Exception('Document type is not SP')

    def get_approve_url(self):
        signer = Signer()
        expired_in = timezone.now() + timedelta(days=1)
        status = 2
        data = {
            'pk': str(self.pk),
            'status': status,
            'expired_in': expired_in.timestamp(),
            'pic': str(self.employee.branch.person_in_charge.pk),

        }
        return f'/document/approve/{signer.sign_object(data)}'

    def get_reject_url(self):
        signer = Signer()
        expired_in = timezone.now() + timedelta(days=1)
        status = 0
        data = {
            'pk': str(self.pk),
            'status': status,
            'expired_in': expired_in.timestamp(),
            'pic': str(self.employee.branch.person_in_charge.pk),
        }
        return f'/document/approve/{signer.sign_object(data)}'

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.representation
