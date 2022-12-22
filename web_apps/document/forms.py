from django import forms
from django.forms import ValidationError
from document.models import Document
from document import utils


class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'document_type',
            'employee',
            'description',
        ]

    def check_pending_document(self):
        if Document.objects.filter(
            employee=self.cleaned_data['employee'],
            document_type=self.cleaned_data['document_type'],
            status=Document.PENDING
        ).exists():
            raise ValidationError(
                f'Employee {self.cleaned_data["employee"]} already has pending document of type {Document.DOCUMENT_TYPES[self.cleaned_data["document_type"]][1]}, please wait for it to be approved or rejected'
            )

    def clean(self):
        self.check_pending_document()
        return super().clean()

    def build_representation(self, obj):
        return [
            obj.serial,
            obj.get_document_type_display(),
            utils.int_to_roman(obj.created_at.month),
            obj.created_at.year,
        ]

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        obj.representation = '/'.join(map(str,
                                          self.build_representation(obj)))
        obj.save()


class DocumentDetailForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'representation',
            'document_type',
            'approved_by',
            'employee',
            'status',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True
