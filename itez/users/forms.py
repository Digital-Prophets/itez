from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Fieldset, Layout, Row, Submit
from crispy_forms.bootstrap import FormActions
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


# class UserRegistrationForm(UserCreationForm):
#     class Meta:

#         model = User
#         exclude = ["created", "password"]
GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Transgender", "Transgender"),
    ("Other", "Other"),
)


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.Field(widget=forms.TextInput(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES
    )
    email = forms.Field(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.Field(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=True
    )
    password2 = forms.Field(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "gender",
            # "user_permissions",
            "email",
            "password1",
            "password2",
        )
