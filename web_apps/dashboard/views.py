from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from document.models import Document
from employee.models import Employee
from leave_request.models import LeaveRequest
from users.decorators import is_authenticated
from branch.models import Branch, HeadQuarter
from django.utils import timezone
# Create your views here.


@method_decorator(is_authenticated, name="dispatch")
class HomePageView(TemplateView):
    template_name = 'home/index.html'

    def build_employee_data(self):
        return {
            'permanent_employee': Employee.objects.filter(
                job_status=1
            ).count(),
            'contract_employee': Employee.objects.filter(
                job_status=0
            ).count(),
            'total_employee': Employee.objects.all().count(),
            'male_employee': Employee.objects.filter(
                gender=0).count(),
            'female_employee': Employee.objects.filter(
                gender=1).count(),
        }

    def build_branch_data(self):
        return {
            'total_branch': Branch.objects.all().count(),
            'total_headquarter': HeadQuarter.objects.all().count(),
        }

    def build_document_data(self):

        dt_now = timezone.now()

        return {
            'total_document': Document.objects.filter(
                created_at__year=dt_now.year).count(),
            'total_document_approved': Document.objects.filter(
                status__in=[0, 2], created_at__year=dt_now.year).count(),
            'total_document_pending': Document.objects.filter(
                status=1, created_at__year=dt_now.year).count(),
        }

    def build_leave_request_data(self):

        dt_now = timezone.now()

        return {
            'total_leave_request': LeaveRequest.objects.filter(
                created_at__year=dt_now.year,
            ).count(),
            'total_leave_request_approved': LeaveRequest.objects.filter(
                status__in=[1, 2, 3], created_at__year=dt_now.year).count(),
            'total_leave_request_pending': LeaveRequest.objects.filter(
                    status=0, created_at__year=dt_now.year).count(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_data'] = self.build_employee_data()
        context['branch_data'] = self.build_branch_data()
        context['document_data'] = self.build_document_data()
        context['leave_request_data'] = self.build_leave_request_data()
        return context
