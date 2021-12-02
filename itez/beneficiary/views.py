# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from itez.beneficiary.models import Beneficiary, Province
from itez.users.models import Profile
from itez.beneficiary.models import Drug
from itez.beneficiary.models import Prescription
from itez.beneficiary.models import District
from itez.beneficiary.models import Lab
from itez.beneficiary.models import Province
from itez.users.models import User

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def list_beneficiary(request):
    beneficiaries = Beneficiary.objects.all()
    beneficiary_list = [beneficiary for beneficiary in beneficiaries]

    context = {"beneficiaries": beneficiary_list}

    html_template = loader.get_template('home/list_beneficiary.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def user_profile(request, id):
    profile_detail = Profile.objects.get(id=request.user.id)
    prescriptions = Prescription.objects.all()
    drugs = Drug.objects.all()
    labs = Lab.objects.all()
    beneficiaries = Beneficiary.objects.all()
    context = {
        "user": profile_detail, 
        "drugs": drugs, 
        "labs": labs, 
        "prescriptions": prescriptions,
        "beneficiaries": beneficiaries
    }
    return render(request, "includes/user-profile.html", context)

@login_required(login_url="/login/")
def user_profile_update(request, id):
    user_profile_detail = Profile.objects.get(id=request.user.id)
    if request.method == "POST":
        phone_no_1  = request.POST.get("phone-no-1", user_profile_detail.phone_number)
        phone_no_2  = request.POST.get("phone-no-2", user_profile_detail.phone_number_2)
        first_name  = request.POST.get("first-name", user_profile_detail.user.first_name)
        last_name = request.POST.get("last-name", user_profile_detail.user.last_name)
        address     = request.POST.get("address", user_profile_detail.address)
        postal_code = request.POST.get("postal-code", user_profile_detail.postal_code)
        city        = request.POST.get("city", user_profile_detail.city)
        email       = request.POST.get("email", user_profile_detail.user.email)
        gender      = request.POST.get("gender", user_profile_detail.gender)
        sex         = request.POST.get("sex", user_profile_detail.sex)
        about       = request.POST.get("about", user_profile_detail.about_me)
        birth_date  = request.POST.get("birth-date", user_profile_detail.about_me)
        photo  = request.FILES.get("filename", user_profile_detail.profile_photo)
        
        user_profile_detail.phone_number    = phone_no_1
        user_profile_detail.phone_number_2  = phone_no_2
        user_profile_detail.user.first_name = first_name
        user_profile_detail.user.last_name  = last_name
        user_profile_detail.user.email      = email
        user_profile_detail.address         = address
        user_profile_detail.postal_code     = postal_code
        user_profile_detail.gender          = gender
        user_profile_detail.sex             = sex
        user_profile_detail.about_me        = about
        user_profile_detail.birth_date      = birth_date
        user_profile_detail.user.city       = city
        user_profile_detail.save()
        return redirect("user_profile", id=id)
    context = {"user": user_profile_detail}    
    return render(request, "includes/edit-user-profile.html", context)

@login_required(login_url="/login/")
def user_events(request):

    context = {"events": []}

    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def beneficiary_report(request):

    context = {"data": []}

    html_template = loader.get_template('home/reports.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    