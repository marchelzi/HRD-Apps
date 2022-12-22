from datetime import datetime
from django import forms
from django.forms import ValidationError

from leave_request.models import LEAVE_TYPES, LeaveDetail, LeaveRequest
from employee.models import Employee


class LeaveRequestForm(forms.Form):
    leave_type = forms.ChoiceField(choices=LEAVE_TYPES)
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all().order_by('full_name'))

    date_range = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'date_range'}), label='Tanggal', required=True,
    )
    reason = forms.CharField(widget=forms.Textarea,
                             label='Alasan', required=True)

    def clean_date_range(self):
        date_range = self.cleaned_data['date_range']
        if not date_range:
            raise forms.ValidationError('Tanggal harus diisi')
        date_range = date_range.split(' to ')
        for date in date_range:
            try:
                datetime.strptime(date, '%d-%m-%Y')
            except ValueError:
                raise forms.ValidationError(
                    'Format tanggal salah, gunakan format dd-mm-yyyy')
        return [datetime.strptime(date, '%d-%m-%Y') for date in date_range]

    def check_leave_quota(self, user: Employee, duration):
        if not hasattr(user, 'leave_balances'):
            raise ValidationError(
                'Karyawan tidak memiliki kuota cuti')
        elif user.leave_balances.total_balance == 0:
            raise ValidationError(
                'Karyawan tidak memiliki kuota cuti')

        elif user.leave_balances.balance == 0:
            raise ValidationError(
                'Kuota cuti anda sudah habis')
        elif user.leave_balances.balance < duration:
            raise ValidationError(
                f'Kuota cuti tidak mencukupi, kuota cuti {user.leave_balances.balance} hari, sedangkan permohonan cuti {duration} hari')

    def check_pending_leave_request(self, user: Employee, dates):
        # get leave request month by dates
        # get month from dates

        pending_leave = user.leave_requests.filter(
            status=LeaveRequest.WAITING_FOR_APPROVAL)
        if pending_leave.exists():
            raise ValidationError(
                'Permohonan tidak dapat diproses. Permohonan cuti yang diajukan pada tanggal {} belum disetujui. Mohon tunggu sampai permohonan cuti disetujui/ditolak/dibatalkan'.format(
                    pending_leave.first().created_at.strftime('%d-%m-%Y')))

    def check_is_user_pic(self, user: Employee):
        user

    def clean(self):
        cleaned_data = super().clean()
        user = self.cleaned_data.get('employee', None)
        dates = self.cleaned_data.get('date_range', None)
        self.check_leave_quota(user, len(dates))
        self.check_pending_leave_request(user, dates)
        return cleaned_data

    def save(self):

        start_date, end_date = self.cleaned_data['date_range'] if len(self.cleaned_data['date_range']) == 2 else [
            self.cleaned_data['date_range'][0], self.cleaned_data['date_range'][0]]

        leave = LeaveRequest.objects.create(
            employee=self.cleaned_data['employee'],
        )
        leave_detail = LeaveDetail.objects.create(
            leave_request=leave,
            leave_type=self.cleaned_data['leave_type'],
            reason=self.cleaned_data['reason'],
            start_date=start_date,
            end_date=end_date,
            duration=(end_date - start_date).days + 1,
        )
        return leave


class LeaveDetailForm(forms.Form):

    employee = forms.CharField(disabled=True)
    approved_by = forms.CharField(disabled=True)
    status = forms.CharField(disabled=True)
    start_date = forms.CharField(disabled=True)
    end_date = forms.CharField(disabled=True)

    reason = forms.CharField(widget=forms.Textarea, disabled=True)

    def __init__(self, leave_request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        leave = leave_request
        self.fields['employee'].initial = leave.employee.full_name
        self.fields['approved_by'].initial = leave.approved_by.full_name if leave.approved_by else ''
        self.fields['status'].initial = leave.get_status_display()
        self.fields['start_date'].initial = leave.leave_details.start_date.strftime(
            '%d-%m-%Y')
        self.fields['end_date'].initial = leave.leave_details.end_date.strftime(
            '%d-%m-%Y')
        self.fields['reason'].initial = leave.leave_details.reason
