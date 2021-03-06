from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView
from itez.authentication.user_roles import user_roles
from itez.users.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from itez.users.models import User as user_model
from itez.users.models import Profile
from itez.beneficiary.models import District, Province
from itez.users.models import EDUCATION_LEVEL, GENDER_CHOICES, SEX_CHOICES
from notifications.signals import notify
from rolepermissions.roles import RolesManager


User = get_user_model()


class UserCreateView(LoginRequiredMixin, CreateView):
    """
    Create an user object.
    """

    model = User
    form_class = UserRegistrationForm
    template_name = "accounts/user_create.html"

    def get_success_url(self):
        return reverse("beneficiary:user_events")

    def form_invalid(self, form):
        print("form is invalid")
        # print(self.request.POST)
        return super(UserCreateView, self).form_invalid(form)

    def form_valid(self, form):
        notify.send(self.request.user, recipient=self.request.user, verb="created user")
        return super(UserCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        roles = RolesManager.get_roles_names()
        user = self.request.user
        all_unread = user.notifications.unread()[:4]
        context["notifications"] = all_unread
        context["title"] = "create user"
        context["roles"] = roles
        context["user_roles"] = user_roles()
        return context


@login_required(login_url="/login/")
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    notify.send(request.user, recipient=request.user, verb="deleted user")
    return redirect(reverse("beneficiary:user_events"))


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


@login_required(login_url="/login/")
def user_profile_photo_update(request):
    current_profile_object = Profile.objects.get(id=request.user.id)
    profile_photo = request.FILES.get(
        "profile-photo", current_profile_object.profile_photo
    )
    current_profile_object.profile_photo = profile_photo
    current_profile_object.save()
    return redirect(reverse("beneficiary:home"))


@login_required(login_url="/login/")
def user_profile(request):
    current_user = user_model.objects.get(id=request.user.id)
    user_profile = Profile.objects.get(id=current_user.id)
    # user_district = District.objects.get(id=user_profile.id)
    # user_province = Province.objects.get(id=user_profile.id)

    if request.method == "POST":
        phone_no_1 = request.POST.get("phone-no-1", user_profile.phone_number)
        phone_no_2 = request.POST.get("phone-no-2", user_profile.phone_number_2)
        first_name = request.POST.get("first-name", user_profile.user.first_name)
        last_name = request.POST.get("last-name", user_profile.user.last_name)
        username = request.POST.get("username", user_profile.user.username)
        address = request.POST.get("address", user_profile.address)
        postal_code = request.POST.get("postal-code", user_profile.postal_code)
        # province = request.POST.get("province", user_province.name)
        # district = request.POST.get("district", user_district.name)
        email = request.POST.get("email", user_profile.user.email)
        gender = request.POST.get("gender", user_profile.gender)
        sex = request.POST.get("sex", user_profile.sex)
        profile_photo = request.FILES.get("profile-photo", user_profile.profile_photo)
        education_level = request.POST.get(
            "education-level", user_profile.education_level
        )
        about = request.POST.get("about", user_profile.about_me)
        birth_date = request.POST.get("birth-date", user_profile.birth_date)
        if birth_date:
            user_profile.birth_date = birth_date

        user_profile.phone_number = phone_no_1
        user_profile.phone_number_2 = phone_no_2
        user_profile.address = address
        user_profile.postal_code = postal_code
        user_profile.gender = gender
        user_profile.sex = sex
        user_profile.education_level = education_level.title()
        user_profile.about_me = about
        user_profile.profile_photo = profile_photo
        user_profile.save()

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        current_user.username = username
        current_user.save()

        # user_district.name = district
        # user_district.save()

        # user_province.name = province
        # user_province.save()
        return redirect("/user/profile")

    education_levels = [level[1] for level in EDUCATION_LEVEL]
    sex_array = [sex[1] for sex in SEX_CHOICES]
    gender_array = [gender[1] for gender in GENDER_CHOICES]
    user = request.user
    all_unread = user.notifications.unread()[:4]
    context = {
        "notifcations": all_unread,
        "user": user_profile,
        "education_levels": education_levels,
        "gender_array": gender_array,
        "sex_array": sex_array,
    }
    return render(request, "includes/user_profile.html", context)


# class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

#     model = User
#     fields = ["name"]
#     success_message = _("Information successfully updated")

#     def get_success_url(self):
#         return self.request.user.get_absolute_url()  # type: ignore [union-attr]

#     def get_object(self):
#         return self.request.user


# user_update_view = UserUpdateView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "accounts/user_update.html"
    success_url = "/events"
    fields = [
        "username",
    ]
    # exclude= ["password"]

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return redirect(reverse("beneficiary:events"))

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        form = UserRegistrationForm(instance=user)
        user = self.request.user
        all_unread = user.notifications.unread()[:4]
        context["notifications"] = all_unread
        context["title"] = "update user"
        context["form"] = form
        context["user_roles"] = user_roles()
        return context
    
        
@login_required(login_url="/login/")
def update_view(request, pk):
    user = User.objects.get(id=pk)
    form = UserRegistrationForm(request.POST or None, instance=user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        return redirect("/events")
    context = {
        "form": form,
        "title": "update_user",
    }
    return render(request, "accounts/user_update.html", context)


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
