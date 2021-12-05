# -*- encoding: utf-8 -*-

from django import template
from django.contrib.gis.db.models import fields
from django.views.generic import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from itez.beneficiary.models import Beneficiary, BeneficiaryParent, MedicalRecord
from itez.beneficiary.models import Service

from itez.beneficiary.forms import BeneficiaryForm, MedicalRecordForm
from itez.users.models import User, Profile
from itez.beneficiary.models import Drug, Prescription, Lab, District, Province


@login_required(login_url="/login/")
def index(request):
    opd = Service.objects.filter(client_type="OPD").count()
    hts = Service.objects.filter(service_type="HTS").count()
    vl = Service.objects.filter(service_type="VL").count()
    art = Service.objects.filter(client_type="ART").count()
    labs = Service.objects.filter(service_type="LAB").count()
    pharmacy = Service.objects.filter(service_type="PHARMACY").count()
    male = Beneficiary.objects.filter(gender="Male").count()
    female = Beneficiary.objects.filter(gender="Female").count()
    transgender = Beneficiary.objects.filter(gender="Transgender").count
    other = Beneficiary.objects.filter(gender="Other").count()

    context = {
        "segment": "index",
        "opd": opd,
        "hts": hts,
        "vl": vl,
        "art": art,
        "labs": labs,
        "pharmacy": pharmacy,
        "male": male,
        "female": female,
        "transgender": transgender,
        "other": other,
    }

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def user_profile(request):
    user_profile_detail = Profile.objects.get(id=request.user.id)
    user_table = User.objects.get(id=request.user.id)
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


@login_required(login_url="/login/")
def uielements(request):
    context = {"title": "UI Elements"}
    html_template = loader.get_template("home/basic-table.html")
    return HttpResponse(html_template.render(context, request))


class MedicalRecordListView(LoginRequiredMixin, ListView):
    template_name = "beneficiary/medical_record_list.html"
    model = MedicalRecord

    def get_queryset(self):
        return MedicalRecord.objects.filter(beneficiary=self.kwargs["beneficiary_id"])

    def get_context_data(self, **kwargs):
        # Benenficiary-098123hjkf/medical_record_list
        context = super(MedicalRecordListView, self).get_context_data(**kwargs)
        context["beneficiary"] = Beneficiary.objects.get(
            pk=self.kwargs["beneficiary_id"]
        )
        context["title"] = "Medical Records"
        return context


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    """
    Display details of a single beneficiary medical record.
    """

    context_object_name = "medical_record"
    template_name = "beneficiary/medical_record_detail.html"
    model = MedicalRecord

    def get_context_data(self, **kwargs):
        context = super(MedicalRecordDetailView, self).get_context_data(**kwargs)
        context["title"] = "Medical Record"
        return context


class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new MedicalRecord
    """

    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = "beneficiary/medical_record_create.html"

    def get_success_url(self):
        return reverse("beneficiary:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MedicalRecordCreateView, self).form_valid(form)


class BeneficiaryCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Beneficiary object.
    """

    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = "beneficiary/beneficiary_create.html"

    def get_success_url(self):
        return reverse("beneficiary:beneficiary_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BeneficiaryCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BeneficiaryCreateView, self).get_context_data(**kwargs)
        context["title"] = "create new beneficiary"
        return context


class BenenficiaryListView(LoginRequiredMixin, ListView):
    """
    Beneficiary  List View.
    """

    context_object_name = "beneficiaries"
    model = Beneficiary
    paginate_by = 10
    template_name = "beneficiary/beneficiary_list.html"

    def get_queryset(self):
        return Beneficiary.objects.filter(alive=True)

    def get_context_data(self, **kwargs):
        context = super(BenenficiaryListView, self).get_context_data(**kwargs)

        beneficiaries = Beneficiary.objects.all()
        context["opd"] = Service.objects.filter(client_type="OPD").count()
        context["hts"] = Service.objects.filter(service_type="HTS").count()
        context["vl"] = Service.objects.filter(service_type="VL").count()
        context["art"] = Service.objects.filter(client_type="ART").count()
        context["labs"] = Service.objects.filter(service_type="LAB").count()
        context["pharmacy"] = Service.objects.filter(service_type="PHARMACY").count()
        context["title"] = "Beneficiaries"
        return context


class BeneficiaryDetailView(LoginRequiredMixin, DetailView):
    """
    Beneficiary Details view.
    """

    context_object_name = "beneficiary"
    model = Beneficiary
    template_name = "beneficiary/beneficiary_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BeneficiaryDetailView, self).get_context_data(**kwargs)

        context["title"] = "Beneficiary Details"
        context["service_title"] = "services"
        context["medication_title"] = "medications"
        context["lab_title"] = "labs"

        return context


@login_required(login_url="/login/")
def user_events(request):
    users = User.objects.all()
    # users_list = [user for user in users]
    page_num = request.GET.get("page", 1)
    p = Paginator(users, 2)

    page_obj = p.get_page(page_num)
    context = {"users_list": page_obj}

    html_template = loader.get_template("home/events.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def beneficiary_report(request):
    opd = Service.objects.filter(client_type="OPD").count()
    hts = Service.objects.filter(service_type="HTS").count()
    vl = Service.objects.filter(service_type="VL").count()
    art = Service.objects.filter(client_type="ART").count()
    labs = Service.objects.filter(service_type="LAB").count()
    pharmacy = Service.objects.filter(service_type="PHARMACY").count()

    context = {
        "data": [],
        "opd": opd,
        "hts": hts,
        "vl": vl,
        "art": art,
        "labs": labs,
        "pharmacy": pharmacy,
    }

    html_template = loader.get_template("home/reports.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


def doughnutChart(request):
    femaleSex = Beneficiary.objects.filter(sex="Female")
    maleSex = Beneficiary.objects.filter(sex="Male")
