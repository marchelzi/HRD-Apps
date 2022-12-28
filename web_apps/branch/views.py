from django import forms
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from ajax_datatable.views import AjaxDatatableView
from branch.models import Branch, HeadQuarter
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django_htmx.http import HttpResponseClientRefresh
from django.contrib import messages
from branch import messages as branch_messages
from django.utils.decorators import method_decorator
from users.decorators import is_authenticated



# Create your views here.

@method_decorator(is_authenticated, name="dispatch")
class BranchHomePage(TemplateView):
    template_name = 'branch/index.html'

@method_decorator(is_authenticated, name="dispatch")
class BranchAjaxDatatable(AjaxDatatableView):
    model = Branch
    length_menu = [10, 25, 50, 100]
    search_values_separator = ' '
    initial_order = [
        ["created_at", "desc"],
    ]

    def get_initial_queryset(self, request):
        return self.model.objects.all()

    def get_column_defs(self, request):
        return [
            {
                "name": "name",
                "title": "Name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "initial",
                "title": "Initial",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "HeadQuarter",
                "title": "HeadQuarter",
                "foreign_field": "headquarter__name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "br_type",
                "title": "Branch Type",
                "visible": True,
                "searchable": True,
                "choices": Branch.BRANCH_TYPES,
            },
            {
                "name": "person_in_charge",
                "title": "PIC",
                "foreign_field": "person_in_charge__full_name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "phone",
                "title": "Phone",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "address",
                "title": "Address",
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
                "name": "actions",
                "title": "Actions",
                "visible": True,
                "searchable": False,
            }
        ]

    def customize_row(self, row, obj):
        row['actions'] = render_to_string(
            'branch/includes/actions.html',
            context={'pk': obj.pk}
        )

@method_decorator(is_authenticated, name="dispatch")
class BranchCreateView(CreateView):
    model = Branch
    fields = '__all__'
    success_url = reverse_lazy('branch:branch')
    template_name = 'branch/includes/create.html'

    def get_context_data(self, **kwargs):
        context = super(BranchCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create Branch'
        return context

    def set_message(self):
        messages.success(
            self.request, branch_messages.BRANCH_CREATED_MESSAGE.format(self.object.name))

    def form_valid(self, form):
        super(BranchCreateView, self).form_valid(form)
        self.set_message()

        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class BranchUpdateView(UpdateView):
    model = Branch
    fields = '__all__'
    success_url = reverse_lazy('branch:branch')
    template_name = 'branch/includes/update.html'

    def get_context_data(self, **kwargs):
        context = super(BranchUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Branch'
        return context

    def set_message(self):
        messages.success(
            self.request, branch_messages.BRANCH_UPDATED_MESSAGE.format(self.object.name))

    def form_valid(self, form):
        super(BranchUpdateView, self).form_valid(form)
        self.set_message()
        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class BranchDeleteView(DeleteView):
    model = Branch
    success_url = reverse_lazy('branch:branch')
    template_name = 'branch/includes/delete.html'

    def get_context_data(self, **kwargs):
        context = super(BranchDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete Branch'
        return context

    def set_message(self):
        messages.success(self.request, branch_messages.BRANCH_DELETED_MESSAGE.format(
            self.object.name
        ))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.set_message()
        self.object.delete()
        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class HeadQuarterPage(TemplateView):
    template_name = 'headquarter/index.html'

@method_decorator(is_authenticated, name="dispatch")
class HeadQuarterAjaxDatatable(AjaxDatatableView):
    model = HeadQuarter
    length_menu = [10, 25, 50, 100]
    search_values_separator = ' '
    initial_order = [
        ["created_at", "desc"],
    ]

    def get_initial_queryset(self, request):
        return self.model.objects.all()

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

@method_decorator(is_authenticated, name="dispatch")
class HeadQuarterCreateView(CreateView):
    model = HeadQuarter
    fields = '__all__'
    success_url = reverse_lazy('branch:headquarter')
    template_name = 'crud/create_update.html'

    def get_context_data(self, **kwargs):
        context = super(HeadQuarterCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create HeadQuarter'
        context['url'] = reverse_lazy('branch:headquarter_create')
        return context

    def set_message(self):
        messages.add_message(self.request, messages.SUCCESS, branch_messages.HQ_CREATED_MESSAGE.format(
            self.object.name))

    def form_valid(self, form):
        super(HeadQuarterCreateView, self).form_valid(form)
        self.set_message()
        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class HeadQuarterUpdateView(UpdateView):
    model = HeadQuarter
    fields = '__all__'
    success_url = reverse_lazy('branch:headquarter')
    template_name = 'crud/create_update.html'

    def get_context_data(self, **kwargs):
        context = super(HeadQuarterUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update HeadQuarter'
        context['url'] = reverse_lazy('branch:headquarter_update', kwargs={
                                      'pk': self.kwargs.get('pk')})
        return context

    def set_message(self):
        messages.add_message(self.request, messages.SUCCESS, branch_messages.HQ_UPDATED_MESSAGE.format(
            self.object.name
        ))

    def form_valid(self, form):
        super(HeadQuarterUpdateView, self).form_valid(form)
        self.set_message()
        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class HeadQuarterDeleteView(DeleteView):
    model = HeadQuarter
    success_url = reverse_lazy('branch:headquarter')
    template_name = 'crud/delete.html'

    def get_context_data(self, **kwargs):
        context = super(HeadQuarterDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete HeadQuarter'
        context['url'] = reverse_lazy('branch:headquarter_delete', kwargs={
                                      'pk': self.kwargs.get('pk')})
        context['message'] = """
        Are you sure you want to delete this HeadQuarter? Deleting this HeadQuarter will also delete all the Branches associated with it.
        """
        return context

    def set_message(self):
        messages.add_message(self.request, messages.SUCCESS,
                             branch_messages.HQ_DELETED_MESSAGE.format(self.object.name))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.set_message()
        self.object.delete()
        return HttpResponseClientRefresh()
