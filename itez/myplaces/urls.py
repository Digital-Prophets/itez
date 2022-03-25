from django.urls import path

from . import views



urlpatterns = [
path('', views.home_page.as_view()),

path('facility', views.facility_home.as_view()),
path('places_data/', views.places_dataset, name='my_places'),
path('facility_detail/<int:pk>/', views.facility_details, name='facility_detail'),
path('beneficiary_home_page', views. beneficiary_home_page, name=' beneficiary_home_page'),
path('beneficiary_list', views.beneficiary_lists, name='beneficiary_list'),
path('beneficiary_detail/<int:pk>/', views.beneficiary_detail, name='beneficiary_detail'),
path('medical_records_list', views.medical_records, name='medical_records_list'),
path('medical_records_detail/<int:pk>/', views.medical_records_detail, name='medical_records_detail'),

]