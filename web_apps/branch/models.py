from django.db import models
from uuid import uuid4

from django.urls import reverse
# Create your models here.


class HeadQuarter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_update_url(self):
        return reverse('branch:headquarter_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('branch:headquarter_delete', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Branch(models.Model):
    BRANCH_TYPES = (
        (0, 'Dalam Kota'),
        (1, 'Luar Kota')
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    initial = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    br_type = models.IntegerField(
        choices=BRANCH_TYPES, default=0, verbose_name='Branch Type')
    headquarter = models.ForeignKey(HeadQuarter, on_delete=models.CASCADE)
    person_in_charge = models.ForeignKey(
        'employee.Employee',
        on_delete=models.SET_NULL,
        related_name='pic',
        null=True, blank=True
    )

    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.initial = self.initial.upper()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'initial')

    def __str__(self):
        return self.name
