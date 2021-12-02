# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.views.generic import TemplateView

from itez.beneficiary.models import Beneficiary


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
def user_events(request):

    context = {"events": []}

    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def beneficiary_report(request):

    male = Beneficiary.objects.filter(gender='Male').count()
    female = Beneficiary.objects.filter(gender='Female').count()
    transgender = Beneficiary.objects.filter(gender='Transgender').count
    other = Beneficiary.objects.filter(gender='Other').count()
    malesex = Beneficiary.objects.filter(sex='Male').count
    femalesex = Beneficiary.objects.filter(sex='Female')

    beneficiarybyyear = Beneficiary.objects.filter(created=["2017-01-01", "2021-12-31"])

    # beneFbyYr = Beneficiary.objects.order_by('date_of_birth')
    # print('-------------------------------------------------------> :',)

    context = {'segment': 'reports', "male": male, "female": female,
               "transgender": transgender, "other": other, "m": malesex, "f": femalesex, "beneficiarybyyear":  beneficiarybyyear}

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
