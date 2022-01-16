from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Fieldset, Layout, Row, Submit
from crispy_forms.bootstrap import FormActions
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from itez.users.models import User
from django.contrib.auth.forms import UserCreationForm


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User



class UserRegistrationForm(UserCreationForm):
    class Meta:

        model = User
        exclude = ["created", "password"]
        
       
