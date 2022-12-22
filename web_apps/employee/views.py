from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from ajax_datatable.views import AjaxDatatableView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django_htmx.http import HttpResponseClientRefresh
from employee.forms import EmployeeDetailForm, EmployeeForm
from django.views.generic import (FormView, TemplateView)
from django.contrib import messages
from employee.models import Employee, Position
from employee import messagess as employee_messages

# Create your views here.


class PositionHomePage(TemplateView):
    template_name = 'position/index.html'


class PositionAjaxDatatable(AjaxDatatableView):
    model = Position
    length_menu = [10, 25, 50, 100]
    search_values_separator = ' '
    initial_order = [
        ['created_at', 'desc'],
    ]

    def get_column_defs(self, request):
        return [
            {
                "name": "name",
                "title": "Name",
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
        row['actions'] = render_to_string(
            'crud/actions.html',
            context={
                'update_url': obj.get_update_url(),
                'delete_url': obj.get_delete_url(),
            }
        )


class PositionCreateView(CreateView):
    model = Position
    fields = '__all__'
    success_url = reverse_lazy('employee:position')
    template_name = 'crud/create_update.html'

    def get_context_data(self, **kwargs):
        context = super(PositionCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Position'
        context['url'] = reverse_lazy('employee:position_create')
        return context

    def set_message(self):
        messages.add_message(self.request, messages.SUCCESS,
                             employee_messages.POSITION_CREATE_MESSAGE.format(
                                 self.object.name)
                             )

    def form_valid(self, form):
        super(PositionCreateView, self).form_valid(form)
        self.set_message()
        return HttpResponseClientRefresh()


class PositionUpdateView(UpdateView):
    model = Position
    fields = '__all__'
    success_url = reverse_lazy('employee:position')
    template_name = 'crud/create_update.html'

    def get_context_data(self, **kwargs):
        context = super(PositionUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Position'
        context['url'] = self.object.get_update_url()
        return context

    def set_message(self):
        messages.add_message(self.request, messages.SUCCESS,
                             employee_messages.POSITION_UPDATE_MESSAGE.format(
                                 self.object.name)
                             )

    def form_valid(self, form):
        super(PositionUpdateView, self).form_valid(form)
        self.set_message()
        return HttpResponseClientRefresh()


class PositionDeleteView(DeleteView):
    model = Position
    success_url = reverse_lazy('employee:position')
    template_name = 'crud/delete.html'

    def get_context_data(self, **kwargs):
        context = super(PositionDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete Position'
        context['url'] = self.object.get_delete_url()
        context['message'] = """
        Are you sure you want to delete this position? Deleting this position will also delete all the employees
        """
        return context

    def set_message(self):
        messages.add_message(self.request, messages.SUCCESS,
                             employee_messages.POSITION_DELETE_MESSAGE.format(self.object.name))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.set_message()
        self.object.delete()
        return HttpResponseClientRefresh()


class EmployeeHomePage(TemplateView):
    template_name = 'employee/index.html'


class EmployeeAjaxDatatable(AjaxDatatableView):
    model = Employee
    length_menu = [10, 25, 50, 100]
    search_values_separator = ' '
    initial_order = [
        ['joint_date', 'desc'],
    ]

    def get_column_defs(self, request):
        return [
            {
                "name": "full_name",
                "title": "Name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "id_number",
                "title": "NIK",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "position",
                "title": "Position",
                "foreign_field": "position__name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "branch",
                "title": "Branch",
                "foreign_field": "branch__name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "headquarter",
                "title": "HQ",
                "foreign_field": "branch__headquarter__name",
                "visible": True,
                "searchable": True,
            },

            {
                "name": "joint_date",
                "title": "Join Date",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "job_status",
                "title": "Status",
                "visible": True,
                "searchable": True,
                "choices": Employee.EMPLOYEE_STATUSES,
            },

            {
                "name": "actions",
                "title": "Actions",
                "visible": True,
                "searchable": False,
            }
        ]

    def customize_row(self, row, obj):
        row['actions'] = f"""
        <div class="btn-group">
        <a href="{obj.get_update_url()}" class="btn btn-sm btn-primary">Update</a>
        <a href="#" onclick="show_modal('{obj.get_delete_url()}')" class="btn btn-sm btn-danger">Delete</a>
        <a href="{obj.get_detail_url()}" class="btn btn-sm btn-primary">Detail</a>

        </div>
        """


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee:employee')
    template_name = 'employee/includes/create_update.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Add a Employee'
        context['url'] = reverse_lazy('employee:employee_create')
        return context

    def set_message(self, form):
        messages.add_message(self.request, messages.SUCCESS, employee_messages.EMPLOYEE_CREATE_MESSAGE.format(
            form.cleaned_data['full_name']
        ))

    def form_valid(self, form):
        self.set_message(form)
        return super(EmployeeCreateView, self).form_valid(form)


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('employee:employee')
    template_name = 'employee/includes/create_update.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Employee'
        context['url'] = self.object.get_update_url()
        return context

    def set_message(self):
        messages.add_message(self.request, messages.SUCCESS, employee_messages.EMPLOYEE_UPDATE_MESSAGE.format(
            self.object.full_name
        ))

    def form_valid(self, form):
        self.set_message()
        return super(EmployeeUpdateView, self).form_valid(form)


class EmployeeDeleteView(DeleteView):
    model = Employee
    success_url = reverse_lazy('employee:employee')
    template_name = 'crud/delete.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete Employee'
        context['url'] = self.object.get_delete_url()
        context['message'] = """
            Are you sure you want to delete this employee? Deleting this employee will also delete all the associated data
            """
        return context

    def set_message(self):
        messages.add_message(self.request, messages.SUCCESS, employee_messages.EMPLOYEE_DELETE_MESSAGE.format(
            self.object.full_name
        ))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.set_message()
        self.object.delete()
        return HttpResponseClientRefresh()


class EmployeeDetailView(FormView):
    form_class = EmployeeDetailForm
    template_name = 'employee/includes/create_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = get_object_or_404(Employee, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee Detail'
        return context
