from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from users.forms import LoginForm, UserChangePasswordForm
from users.models import User
from users.forms import UserCreateForm, UserUpdateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import (FormView, TemplateView)
from ajax_datatable.views import AjaxDatatableView
from django_htmx.http import HttpResponseClientRefresh
from django.utils.decorators import method_decorator
from users.decorators import is_authenticated



# Create your views here.

@method_decorator(is_authenticated, name="dispatch")
class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy("dashboard:index")
    template_name = "accounts/login.html"

    def form_valid(self, form: LoginForm) -> HttpResponse:
        """Process user login"""

        credentials = form.cleaned_data

        user = authenticate(
            email=credentials["email"], password=credentials["password"]
        )
        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(
                self.request,
                messages.INFO,
                "Wrong credentials or your account is inactive",
            )
            return render(self.request, self.template_name, {"form": form})


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy("users:login"))

@method_decorator(is_authenticated, name="dispatch")
class UserIndexView(TemplateView):
    template_name = 'users/index.html'

@method_decorator(is_authenticated, name="dispatch")
class UserAjaxDatatable(AjaxDatatableView):
    model = User
    length_menu = [10, 25, 50, 100]
    search_values_separator = ' '
    initial_order = [
        ['full_name', 'desc'],
    ]

    def get_column_defs(self, request):
        return [
            {
                "name": "full_name",
                "title": "Full Name",
                "visible": True,
                "searchable": True,
            },
            {
                "name": "email",
                "title": "Email",
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
            <a href="#" onclick="show_modal('{reverse_lazy('users:user_update', kwargs={'pk': obj.pk})}')" class="btn btn-sm btn-primary">Update</a>
            <a href="#" onclick="show_modal('{reverse_lazy('users:user_delete', kwargs={'pk': obj.pk})}')" class="btn btn-sm btn-danger">Delete</a>
            <a href="#" onclick="show_modal('{reverse_lazy('users:user_change_password', kwargs={'pk': obj.pk})}')" class="btn btn-sm btn-warning">Change Password</a>
        </div>
        """

@method_decorator(is_authenticated, name="dispatch")
class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'crud/create_update.html'
    success_url = reverse_lazy('users:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create User'
        context['url'] = reverse_lazy('users:user_create')
        return context

    def set_message(self):
        messages.add_message(self.request, messages.INFO,
                             f'{self.object.full_name} has been created')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        super().form_valid(form)
        self.set_message()
        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'crud/create_update.html'
    success_url = reverse_lazy('users:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        context['url'] = reverse_lazy('users:user_update', kwargs={
                                      'pk': self.get_object().pk})
        context['title'] = 'Update User'
        return context

    def set_message(self):
        messages.add_message(self.request, messages.INFO,
                             f'{self.get_object().full_name} has been updated')

    def form_valid(self, form):
        self.set_message()
        super().form_valid(form)
        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class UserChangePasswordView(UpdateView):
    model = User
    form_class = UserChangePasswordForm
    template_name = 'crud/create_update.html'
    success_url = reverse_lazy('users:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        context['url'] = reverse_lazy('users:user_change_password', kwargs={
                                      'pk': self.get_object().pk})
        context['title'] = 'Change Password'
        return context

    def set_message(self):
        messages.add_message(self.request, messages.INFO,
                             f'{self.get_object().full_name} password has been changed')

    def form_valid(self, form):
        self.set_message()
        super().form_valid(form)
        return HttpResponseClientRefresh()

@method_decorator(is_authenticated, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    template_name = 'crud/delete.html'
    success_url = reverse_lazy('users:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete User'
        context['message'] = f'Are you sure you want to delete {self.get_object().full_name}?'
        context['url'] = reverse_lazy('users:user_delete', kwargs={
                                      'pk': self.get_object().pk})
        return context

    def set_message(self):
        messages.add_message(self.request, messages.INFO,
                             f'{self.get_object().full_name} has been deleted')

    def delete(self, request, *args, **kwargs):
        self.set_message()
        super().delete(request, *args, **kwargs)
        return HttpResponseClientRefresh()
