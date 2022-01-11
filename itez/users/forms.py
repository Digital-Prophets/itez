from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Fieldset, Layout, Row, Submit
from crispy_forms.bootstrap import FormActions
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from itez.users.models import User



class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


# class UserCreationForm(admin_forms.UserCreationForm):
#     class Meta(admin_forms.UserCreationForm.Meta):
#         model = User

#         error_messages = {
#             "username": {"unique": _("This username has already been taken.")}
#         }
class UserCreationForm(ModelForm):
    class Meta:

        model = User
        exclude = ["created"]
       

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_tag = False
    #     self.helper.layout = Layout(
    #         Fieldset(
    #             "User Details",
    #             Row(
    #                 Div("username", css_class="form-group col-md-6 mb-0"),
    #                 Div("password", css_class="form-group col-md-6 mb-0"),
    #                 Div("first_name", css_class="form-group col-md-6 mb-0"),
    #                 Div("last_name", css_class="form-group col-md-6 mb-0"),
    #                 Div("email", css_class="form-group col-md-6 mb-0"),
    #                 Div("is_superuser", css_class="form-group col-md-6 mb-0"),
    #                 Div("is_staff", css_class="form-group col-md-6 mb-0"),
    #                 Div("is_active", css_class="form-group col-md-6 mb-0"),
    #                 # Div("date_joined", css_class="form-group col-md-6 mb-0"),
    #                 # Div("date", css_class="form-group col-md-6 mb-0"),
    #             ),
    #         ),
            
    #         FormActions(
    #             Submit("submit", "Create User"),
    #             HTML('<a class="btn btn-danger" href="/events">Cancel</a>'),
    #         ),
    #     )

    # def save(self, commit=True):
    #     instance = super(UserCreationForm, self).save(commit=False)
    #     if commit:
    #         instance.save()
    #     # self.save_m2m()  # we  can use this if we have many to many field on the model i.e Service
    #     return instance
