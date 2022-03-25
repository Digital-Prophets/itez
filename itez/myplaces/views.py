
from importlib.resources import contents
from django.views import generic # django generic view

from django.contrib.gis.geos import fromstr, Point #to get our longitude and latitude

from django.contrib.gis.db.models.functions import Distance #distance between us and fav places

from .models import Myplaces, Beneficiary,MedicalRecord

from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect

from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required


longitude =27.8493049

latitude = -13.1403507 
 

my_location = Point(longitude, latitude, srid=4326) #default location we will use gps geolocation in future totorials.



class home_page(generic.ListView):
    # home_page_list = Beneficiary.objects.all()
    model = Myplaces

    context_object_name = 'places'

    queryset = Myplaces.objects.annotate(distance=Distance('location',

    my_location)

    ).order_by('distance')[0:6]
    template_name = 'home/index.html'

def places_dataset(request):

    place = serialize('geojson', Myplaces.objects.all())

    return HttpResponse(place, content_type='json')




class facility_home(generic.ListView):

    model = Myplaces

    context_object_name = 'places'

    queryset = Myplaces.objects.annotate(distance=Distance('location',

    my_location)

    ).order_by('distance')[0:6]
    template_name = 'beneficiary/beneficiary_page.html'

@login_required(login_url="/login/")
def places_dataset(request):
    place = serialize('geojson', Myplaces.objects.all())
    return HttpResponse(place, content_type='json')



@login_required(login_url="/login/")
def facility_details(request, pk):
    facility_details = get_object_or_404(Myplaces, pk=pk)
    return render(request,"beneficiary/facility_detail.html", {'facility_details': facility_details})



@login_required(login_url="/login/")
def beneficiary_home_page(request):
    return render(request, 'beneficiary/beneficiary_home_page.html')

@login_required(login_url="/login/")
def beneficiary_lists(request):
    itez_app_beneficiary = Beneficiary.objects.all()
    return render(request, 'beneficiary/beneficiary_list.html', {'itez_app_beneficiary': itez_app_beneficiary})


@login_required(login_url="/login/")
def beneficiary_detail(request, pk):
    beneficiary_details = get_object_or_404(Beneficiary, pk=pk)
    return render(request, 'beneficiary/beneficary_detail.html', {'beneficiary_details':  beneficiary_details})



@login_required(login_url="/login/")
def medical_records(request):
    medical_records_lists = MedicalRecord.objects.all()
    return render(request, 'beneficiary/medical_report_list.html', {'medical_records_lists': medical_records_lists})





@login_required(login_url="/login/")
def medical_records_detail(request, pk):
    medical_records_details = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'beneficiary/medical_records_detail.html', {'medical_records_details':  medical_records_details})