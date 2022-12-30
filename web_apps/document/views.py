import time
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from ajax_datatable.views import AjaxDatatableView
from django.views.generic.edit import CreateView, UpdateView
from django_htmx.http import HttpResponseClientRefresh
from document.forms import DocumentCreateForm, DocumentDetailForm
from document.models import Document
from django.views import View
from django.shortcuts import get_object_or_404
from document import tools
from django.core.signing import Signer
from django.contrib import messages
from document import messages as document_messages
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from users.decorators import is_authenticated


# Create your views here.

@method_decorator(is_authenticated, name="dispatch")
class DocumentHomePage(TemplateView):
    template_name = 'document/index.html'


@method_decorator(is_authenticated, name="dispatch")
class DocumentAjaxDatatable(AjaxDatatableView):
    model = Document
    length_menu = [10, 25, 50, 100]
    search_values_separator = ' '
    initial_order = [
        ["created_at", "desc"],
    ]

    def get_column_defs(self, request):
        return [
            {
                "name": "representation",
                "title": "DOC",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "employee",
                "title": "Employee",
                "foreign_field": "employee__full_name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "approved_by",
                "title": "Approver",
                "foreign_field": "approved_by__full_name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "document_type",
                "title": "Document Type",
                "visible": True,
                "searchable": True,
                "choices": Document.DOCUMENT_TYPES,
            },
            {
                "name": "status",
                "title": "Status",
                "visible": True,
                "searchable": True,
                "choices": Document.STATUS_TYPES,
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
        row['actions'] = f"""
        <div class="btn-group">
            <a href="{reverse_lazy('document:document_download', kwargs={'pk': obj.id})}" class="btn btn-sm btn-primary">Download</a>
            <a href="#" onclick="show_modal('{reverse_lazy('document:document_update', kwargs={'pk': obj.id})}')" class="btn btn-sm btn-secondary">Update</a>
            <a href="{reverse_lazy('document:document_send', kwargs={'pk': obj.id})}" class="btn btn-sm btn-green">Send to PIC</a>

        </div>
        """


@method_decorator(is_authenticated, name="dispatch")
class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentCreateForm
    template_name = 'crud/create_update.html'
    success_url = reverse_lazy('document:document_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Document'
        context['url'] = reverse_lazy('document:document_create')
        return context

    def set_message(self):
        messages.add_message(self.request, messages.INFO,
                             document_messages.DOCUMENT_CREATED_MESSAGES_WEB)

    def form_valid(self, form):
        self.object = form.save()
        self.set_message()
        return HttpResponseClientRefresh()


@method_decorator(is_authenticated, name="dispatch")
class DocumentUpdateView(UpdateView):
    model = Document
    fields = ('description', )
    template_name = 'crud/create_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Document'
        context['url'] = reverse_lazy(
            'document:document_update', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseClientRefresh()


@method_decorator(is_authenticated, name="dispatch")
class DocumentGenerator(View):

    def get_queryset(self, **kwargs):
        return get_object_or_404(Document, id=kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset(**kwargs)
        if obj.status == Document.APPROVED:
            # return file
            generated_file = tools.build_spk(
                obj) if obj.document_type == Document.DOCUMENT_TYPES[0][0] else tools.build_sp(obj)
            response = HttpResponse(
                generated_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            # return file
            response['Content-Disposition'] = f'attachment; filename="{obj.representation}.docx"'

            return response
        else:
            messages.add_message(self.request, messages.ERROR,
                                 document_messages.DOCUMENT_NOT_APPROVED_MESSAGES_WEB.format(
                                     obj.representation
                                 ))
            return HttpResponseRedirect(reverse_lazy('document:document'))


@method_decorator(is_authenticated, name="dispatch")
class DocumentInfoToPIC(View):
    success_url = reverse_lazy('document:document')

    def get_queryset(self, **kwargs):
        return get_object_or_404(Document, id=kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset(**kwargs)
        if obj.employee.branch.person_in_charge is not None:
            tools.send_document_to_pic.apply_async(args=(
                obj.id, self.request.build_absolute_uri('/')))
        else:
            messages.add_message(self.request, messages.ERROR,
                                 document_messages.DOCUMENT_PIC_NOT_FOUND_MESSAGES_WEB.format(
                                     obj.employee.branch.name
                                 ))
        return HttpResponseRedirect(self.success_url)


class DocumentApproveView(View):
    success_url = reverse_lazy('document:document')
    template_name = 'document/approve.html'

    def get_queryset(self, pk):
        return get_object_or_404(Document, id=pk)

    def get_context_data(self, pk):
        context = {}
        context['object'] = self.get_queryset(pk)
        context['form'] = DocumentDetailForm(instance=context['object'])
        return context

    def unsign(self, signature):
        try:
            signer = Signer()
            return signer.unsign_object(signature)
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
        messages.add_message(self.request, messages.INFO, message)

    def get(self, request, *args, **kwargs):
        if self.check_expired(kwargs.get('token')):
            return HttpResponseNotFound()
        token_obj = self.unsign(kwargs.get('token'))

        obj = self.get_queryset(token_obj['pk'])
        if obj.status == Document.CANCELED:
            self.set_message('Document has been canceled')
        else:
            obj.status = token_obj['status']
            obj.approved_by_id = token_obj['pic']
            obj.save()
        return TemplateResponse(request, self.template_name, self.get_context_data(token_obj['pk']))
