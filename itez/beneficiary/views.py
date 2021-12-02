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
from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from itez.beneficiary.models import Beneficiary, BeneficiaryParent, MedicalRecord
from itez.beneficiary.models import Service

from itez.beneficiary.forms import BeneficiaryForm, MedicalRecordForm
from itez.users.models import User


@login_required(login_url="/login/")
def index(request):
    opd = Service.objects.filter(client_type='OPD').count()
    hts = Service.objects.filter(service_type='HTS').count()
    vl = Service.objects.filter(service_type='VL').count()
    art = Service.objects.filter(client_type='ART').count()    
    labs = Service.objects.filter(service_type='LAB').count()
    pharmacy = Service.objects.filter(service_type='PHARMACY').count()
    male = Beneficiary.objects.filter(gender = 'Male').count()
    female = Beneficiary.objects.filter(gender = 'Female').count()
    transgender = Beneficiary.objects.filter(gender = 'Transgender').count
    other = Beneficiary.objects.filter(gender = 'Other').count()
   
    context = {'segment': 'index', "opd": opd, "hts": hts, "vl": vl, "art": art, "lab": labs, "pharmacy": pharmacy, "male": male, "female": female, "transgender": transgender, "other": other}
    

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
    
@login_required(login_url="/login/")
def uielements(request):    
    context = {'title': 'UI Elements'}
    html_template = loader.get_template('home/basic-table.html')
    return HttpResponse(html_template.render(context, request))


class MedicalRecordListView(LoginRequiredMixin, ListView):
    template_name = 'beneficiary/medical_record_list.html'
    model = MedicalRecord

    def  get_queryset(self):
        return MedicalRecord.objects.filter(beneficiary=self.kwargs['beneficiary_id'])

    def get_context_data(self, **kwargs):
        # Benenficiary-098123hjkf/medical_record_list
        context = super(MedicalRecordListView, self).get_context_data(**kwargs)
        context['beneficiary'] = Beneficiary.objects.get(pk=self.kwargs['beneficiary_id'])
        context['title'] = 'Medical Records'
        return context


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    """
    Display details of a single beneficiary medical record.
    """
    context_object_name = 'medical_record'
    template_name = 'beneficiary/medical_record_detail.html'
    model = MedicalRecord


    def get_context_data(self, **kwargs):
        context = super(MedicalRecordDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Medical Record'
        return context


class  MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new MedicalRecord
    """
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'beneficiary/medical_record_create.html'

    def get_success_url(self):
        return reverse('beneficiary:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(MedicalRecordCreateView, self).form_valid(form)
    


class  BeneficiaryCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new Beneficiary object.
    """
    
    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = 'beneficiary/beneficiary_create.html'

    def get_success_url(self):
        return reverse('beneficiary:beneficiary_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BeneficiaryCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BeneficiaryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'create new beneficiary'
        return context



class BenenficiaryListView(LoginRequiredMixin, ListView):
    """
    Beneficiary  List View.
    """

    context_object_name = 'beneficiaries'
    model = Beneficiary
    paginate_by = 10
    template_name = 'beneficiary/beneficiary_list.html'

    def  get_queryset(self):
        return Beneficiary.objects.filter(alive=True)

    def get_context_data(self, **kwargs):
        context = super(BenenficiaryListView, self).get_context_data(**kwargs)

        beneficiaries = Beneficiary.objects.all()
        context['opd'] = Service.objects.filter(client_type='OPD').count()
        context['hts'] = Service.objects.filter(service_type='HTS').count()
        context['vl'] = Service.objects.filter(service_type='VL').count()
        context['art'] = Service.objects.filter(client_type='ART').count()    
        context['labs'] = Service.objects.filter(service_type='LAB').count()
        context['pharmacy'] = Service.objects.filter(service_type='PHARMACY').count()
        context['title'] = 'Beneficiaries'
        return context



class BeneficiaryDetailView(LoginRequiredMixin, DetailView):
    """
    Beneficiary Details view.
    """
    context_object_name = 'beneficiary'
    model = Beneficiary
    template_name = 'beneficiary/beneficiary_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BeneficiaryDetailView, self).get_context_data(**kwargs)

        context['title'] = 'Beneficiary Details'
        context['service_title'] = 'services'
        context['medication_title'] = 'medications'
        context['lab_title'] = 'labs'
        
        return context
 
@login_required(login_url="/login/")
def user_events(request):
    users = User.objects.all()
    # users_list = [user for user in users]
    page_num =  request.GET.get('page', 1)
    p = Paginator(users, 2)
    
    page_obj = p.get_page(page_num)
    context = {"users_list": page_obj}

    html_template = loader.get_template('home/events.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def beneficiary_report(request):
    opd = Service.objects.filter(client_type='OPD').count()
    hts = Service.objects.filter(service_type='HTS').count()
    vl = Service.objects.filter(service_type='VL').count()
    art = Service.objects.filter(client_type='ART').count()    
    labs = Service.objects.filter(service_type='LAB').count()
    pharmacy = Service.objects.filter(service_type='PHARMACY').count()

    context = {"data": [], "opd": opd, "hts": hts, "vl": vl, "art": art, "lab": labs, "pharmacy": pharmacy}

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


def doughnutChart(request):
    femaleSex = Beneficiary.objects.filter(sex = 'Female')
    maleSex = Beneficiary.objects.filter(sex = 'Male')


    




