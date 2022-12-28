
import time
from ajax_datatable.views import AjaxDatatableView
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (FormView, TemplateView)
from django.template.loader import render_to_string
from leave_request import tools
from leave_request.forms import LeaveDetailForm, LeaveRequestForm
from django_htmx.http import HttpResponseClientRefresh

from leave_request.models import LeaveDetail, LeaveRequest
from django.core.signing import Signer
from django.template.response import TemplateResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from users.decorators import is_authenticated




# Create your views here.

@method_decorator(is_authenticated, name="dispatch")
class LeaveRequestHomeView(TemplateView):
    template_name = 'leave_request/index.html'

@method_decorator(is_authenticated, name="dispatch")
class LeaveRequestAjaxDatatable(AjaxDatatableView):
    model = LeaveRequest
    length_menu = [10, 25, 50, 100]
    search_values_separator = ' '
    initial_order = [
        ['created_at', 'desc'],
    ]

    def get_column_defs(self, request):
        return [
            {
                "name": "employee",
                "title": "Employee",
                'foreign_field': 'employee__full_name',
                "visible": True,
                "searchable": True,
            },
            {
                "name": "status",
                "title": "Status",
                "visible": True,
                "searchable": True,
                'choices': LeaveRequest.APPROVER_STATUS
            },
            {
                "name": "approved_by",
                "title": "Approved By",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "created_at",
                "title": "Created At",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "updated_at",
                "title": "Updated At",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "actions",
                "title": "Actions",
                "visible": True,
                "searchable": False,
            }
        ]

    def customize_row(self, row, obj):

        row['actions'] = f'''
        <div class="btn-group">
            <a href="#" onclick="show_modal('{obj.get_detail_url()}')" class="btn btn-sm btn-primary">Detail</a>
            <a href="{reverse_lazy('leave_request:leave_send', kwargs={'pk': obj.id})}" class="btn btn-sm btn-green">Send to PIC</a>
        </div>

        '''

        return row

@method_decorator(is_authenticated, name="dispatch")
class LeaveRequestCreateView(FormView):
    template_name = 'leave_request/form.html'
    form_class = LeaveRequestForm
    success_url = reverse_lazy('leave_request:leave_request')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Leave Request'
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class LeaveRequestDetailView(FormView):
    template_name = 'leave_request/detail.html'
    form_class = LeaveDetailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['leave_request'] = get_object_or_404(
            LeaveRequest, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Leave Request Detail'
        return context

@method_decorator(is_authenticated, name="dispatch")
class LeaveInfoToPIC(View):
    success_url = reverse_lazy('leave_request:leave_request')

    def get_queryset(self, pk):
        return get_object_or_404(LeaveRequest, id=pk)

    def get(self, request, *args, **kwargs):
        leave_request = self.get_queryset(kwargs.get('pk'))
        tools.send_document_to_pic(
            leave_request, self.request.build_absolute_uri('/'))
        return HttpResponseRedirect(self.success_url)

@method_decorator(is_authenticated, name="dispatch")
class LeaveApproveView(View):
    success_url = reverse_lazy('leave_request:leave_request')
    template_name = 'leave_request/approve.html'

    def get_queryset(self, pk):
        return get_object_or_404(LeaveRequest, id=pk)

    def get_context_data(self, pk, **kwargs):
        context = {}
        context['object'] = self.get_queryset(pk)
        context["form"] = LeaveDetailForm(
            leave_request=context['object'])
        return context

    def unsign(self, signature):
        try:
            signer = Signer()
            unsigner_object = signer.unsign_object(signature)
            return unsigner_object
        except:
            return HttpResponseNotFound()

    def check_expired(self, signature):
        timestamp_now = int(time.time())
        token_obj = self.unsign(signature)
        if 'expired_in' in token_obj:
            timestamp = token_obj['expired_in']
            if timestamp_now > timestamp:
                return True
            return False
        return True

    def set_message(self, message):
        messages.success(self.request, f'{message}')

    def get(self, request, *args, **kwargs):
        if self.check_expired(kwargs.get('token')):
            return HttpResponseNotFound()
        token_obj = self.unsign(kwargs.get('token'))
        leave_request = self.get_queryset(token_obj['pk'])
        if leave_request.status == 3:
            self.set_message(
                'Leave Request Cancelled, please create new leave request')
        else:
            leave_request.approved_by_id = token_obj['pic']
            leave_request.status = token_obj['status']
            leave_request.save()
        context = self.get_context_data(token_obj['pk'])
        return TemplateResponse(request, self.template_name, context)
