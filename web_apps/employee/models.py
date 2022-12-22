from uuid import uuid4
from django.db import models
from django.urls import reverse

# Create your models here.


class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_update_url(self):
        return reverse('employee:position_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('employee:position_delete', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Position, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Employee(models.Model):
    # Employee Model
    MARITAL_TYPES = (
        (0, 'Belum Menikah'),
        (1, 'Menikah'),
        (2, 'Cerai'),
    )
    RELIGION_TYPES = (
        (0, 'Islam'),
        (1, 'Kristen'),
        (2, 'Katolik'),
        (3, 'Hindu'),
        (4, 'Budha'),
        (5, 'Konghucu'),
    )
    EMPLOYEE_STATUSES = (
        (0, 'Tetap'),
        (1, 'Kontrak'),
    )
    GENDER_TYPES = (
        (0, 'Pria'),
        (1, 'Wanita'),
    )
    EDUCATION_TYPES = (
        (0, 'SD'),
        (1, 'SMP'),
        (2, 'SMA'),
        (3, 'D1'),
        (4, 'D2'),
        (5, 'D3'),
        (6, 'D4'),
        (7, 'S1'),
        (8, 'S2'),
        (9, 'S3'),
        (10, 'Lainnya'),
        (11, 'Tidak Sekolah'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    full_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True, unique=True)
    personal_id_number = models.CharField(max_length=50, unique=True)
    id_number = models.CharField(max_length=50, unique=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    marital_status = models.IntegerField(choices=MARITAL_TYPES, default=0)
    religion = models.IntegerField(choices=RELIGION_TYPES, default=0)
    job_status = models.IntegerField(choices=EMPLOYEE_STATUSES, default=0)
    joint_date = models.DateField()
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)

    gender = models.IntegerField(choices=GENDER_TYPES, default=0)
    education = models.IntegerField(choices=EDUCATION_TYPES, default=0)
    address_by_id = models.CharField(max_length=255)
    address_by_domicile = models.CharField(max_length=255)

    branch = models.ForeignKey(
        'branch.Branch', on_delete=models.CASCADE, null=True, blank=True
    )

    signature = models.ImageField(
        upload_to='signatures', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_update_url(self):
        return reverse('employee:employee_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('employee:employee_delete', kwargs={'pk': self.pk})

    def get_detail_url(self):
        return reverse('employee:employee_detail', kwargs={'pk': self.pk})

    def is_pic_branch(self):
        return self.pic.all().exists()

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.upper()
        self.email = self.email.lower()
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name
