from django import forms

from users.models import User
from django.contrib.auth.password_validation import validate_password


class LoginForm(forms.Form):
    """Create a form for login .

    Args:
        forms ([type]): [description]
    """

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": "Email", "class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'password',
        ]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
        ]


class UserChangePasswordForm(forms.ModelForm):
    """Create a form for change password .

    Args:
        forms ([type]): [description]
    """

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ["password", "password2"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("Password does not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
