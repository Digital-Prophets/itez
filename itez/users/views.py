from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from itez.users.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from itez.users.models import User as user_model
from itez.users.models import Profile
from itez.beneficiary.models import District, Province

User = get_user_model()


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()

@login_required(login_url="/login/")
def user_profile(request):
    user_profile_detail = Profile.objects.get(id=request.user.id)
    user_table = user_model.objects.get(id=request.user.id)
    district_table = District.objects.get(id=request.user.id)
    province_table = Province.objects.get(id=request.user.id)
    if request.method == "POST":
        phone_no_1 = request.POST.get("phone-no-1", user_profile_detail.phone_number)
        phone_no_2 = request.POST.get("phone-no-2", user_profile_detail.phone_number_2)
        first_name = request.POST.get("first-name", user_profile_detail.user.first_name)
        last_name = request.POST.get("last-name", user_profile_detail.user.last_name)
        username = request.POST.get("username", user_profile_detail.user.username)
        address = request.POST.get("address", user_profile_detail.address)
        postal_code = request.POST.get("postal-code", user_profile_detail.postal_code)
        province = request.POST.get("province", province_table.name)
        district = request.POST.get("district", district_table.name)
        email = request.POST.get("email", user_profile_detail.user.email)
        gender = request.POST.get("gender", user_profile_detail.gender)
        sex = request.POST.get("sex", user_profile_detail.sex)
        profile_photo = request.FILES.get("profile-photo", user_profile_detail.profile_photo)
        education_level = request.POST.get("education-level", user_profile_detail.education_level)
        about = request.POST.get("about", user_profile_detail.about_me)
        birth_date = request.POST.get("birth-date", user_profile_detail.birth_date)
        if birth_date:
            user_profile_detail.birth_date = birth_date

        user_profile_detail.phone_number = phone_no_1
        user_profile_detail.phone_number_2 = phone_no_2
        user_profile_detail.address = address
        user_profile_detail.postal_code = postal_code
        user_profile_detail.gender = gender
        user_profile_detail.sex = sex
        user_profile_detail.education_level = education_level.title()
        user_profile_detail.about_me = about
        user_profile_detail.profile_photo = profile_photo
        user_profile_detail.save()
        
        user_table.first_name = first_name
        user_table.last_name = last_name
        user_table.email = email
        user_table.username = username 
        user_table.save()

        district_table.name = district
        district_table.save()

        province_table.name = province
        province_table.save()
        return redirect("/user/profile")
    education_levels = [level.lower() for level in ["None","Primary","Basic","Secondary O'Level","Certificate","Diploma","Degree","Masters","Doctrate","PHD"]]
    sex_array = ["Male", "Female"]
    gender_array = ["Male", "Female", "Transgender", "Other"]
    context = {
        "province": province_table,
        "user": user_profile_detail,
        "education_levels": education_levels,
        "gender_array": gender_array,
        "sex_array": sex_array
    }
    return render(request, "includes/user_profile.html", context)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
