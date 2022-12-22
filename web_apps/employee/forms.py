import re
from django import forms
from employee.models import Employee
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Row, Column, Submit


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = [
            'full_name',
            'email',
            'id_number',
            'personal_id_number',
            'branch',
            'position',
            'phone',
            'gender',
            'address_by_id',
            'address_by_domicile',
            'birth_place',
            'birth_date',
            'marital_status',
            'religion',
            'education',
            'joint_date',
            'job_status',
            'signature',
        ]
        labels = {
            'id_number': 'NIK(Nomor Induk Kependudukan)',
            'personal_id_number': 'NIK(Nomor Induk Karyawan)',
            'address_by_id': 'Address(KTP)',
            'address_by_domicile': 'Address(Domisili)',
            'job_status': 'Status Employee',
        }
        widgets = {
            'joint_date': forms.DateInput(attrs={'type': 'date'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('id_number', css_class='form-group col-md-6 mb-0'),
                Column('personal_id_number',
                       css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('branch', css_class='form-group col-md-6 mb-0'),
                Column('position', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('gender', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('address_by_id', css_class='form-group col-md-6 mb-0'),
                Column('address_by_domicile',
                       css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('birth_place', css_class='form-group col-md-6 mb-0'),
                Column('birth_date', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('marital_status', css_class='form-group col-md-6 mb-0'),
                Column('religion', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('education', css_class='form-group col-md-6 mb-0'),
                Column('joint_date', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('job_status', css_class='form-group col-md-6 mb-0'),
                Column('signature', css_class='form-group col-md-6 mb-0'),
            ),
            Submit('submit', 'Submit'),
        )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        regex = r'([\[\(])?(?:(\+62)|62|0)\1? ?-? ?8(?!0|4|6)\d(?!0)\d\1? ?-? ?\d{3,4} ?-? ?\d{3,5}(?: ?-? ?\d{3})?\b'
        if not phone.startswith('+62'):
            raise forms.ValidationError('Phone number must start with +62')
        if not re.match(regex, phone):
            raise forms.ValidationError('Phone number is not valid')
        return phone

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if not id_number.isdigit():
            raise forms.ValidationError('NIK must be numeric')
        return id_number

    def clean_personal_id_number(self):
        personal_id_number = self.cleaned_data.get('personal_id_number')
        if not personal_id_number.isdigit():
            raise forms.ValidationError('NIK must be numeric')
        # check for duplicate personal_id_number
        return personal_id_number


class EmployeeDetailForm(EmployeeForm):
    leave_total = forms.IntegerField(
        label='Leave Total(This Year)', required=False)
    leave_balance = forms.IntegerField(
        label='Leave Balance(This Year)', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('id_number', css_class='form-group col-md-6 mb-0'),
                Column('personal_id_number',
                       css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('branch', css_class='form-group col-md-6 mb-0'),
                Column('position', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('gender', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('address_by_id', css_class='form-group col-md-6 mb-0'),
                Column('address_by_domicile',
                       css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('birth_place', css_class='form-group col-md-6 mb-0'),
                Column('birth_date', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('marital_status', css_class='form-group col-md-6 mb-0'),
                Column('religion', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('education', css_class='form-group col-md-6 mb-0'),
                Column('joint_date', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('job_status', css_class='form-group col-md-6 mb-0'),
                Column('signature', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('leave_total', css_class='form-group col-md-6 mb-0'),
                Column('leave_balance', css_class='form-group col-md-6 mb-0'),
            ),

        )
        if hasattr(self.instance, 'leave_balances'):
            self.fields['leave_total'].initial = self.instance.leave_balances.total_balance
            self.fields['leave_balance'].initial = self.instance.leave_balances.balance
        else:
            self.fields['leave_total'].initial = 0
            self.fields['leave_balance'].initial = 0
