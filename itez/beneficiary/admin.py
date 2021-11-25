from django.contrib import admin
from itez.beneficiary.models import (
    Lab,
    Drug,
    Province,
    District,
    Prescription,

    ServiceArea,
    WorkDetail,
    AgentDetail,
    Beneficiary,
    BeneficiaryParent,
    Facility,
    FacilityType,
    ImplementingPartner,
    Service,
    ServiceProviderPersonel,
    ServiceProviderPersonelQualification
)

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class LabResource(resources.ModelResource):
    class Meta:
        model = Lab

@admin.register(Lab)
class LabAdmin(ImportExportModelAdmin):
    resource_class = LabResource

    list_display = (
        'title', 
        'date'
        )

    search_fields = (
        'title', 
        'facility__name', 
        'beneficiary__beneficiary_id', 
        )

class DrugResource(resources.ModelResource):
    class Meta:
        model = Drug

@admin.register(Drug)
class DrugAdmin(ImportExportModelAdmin):
    resource_class = DrugResource

    list_display = (
        'name', 
        'manufacturer', 
        'expiry_date'
        )

    search_fields = (
        'name', 
        'beneficiary__beneficiary_id', 
        )

class PrescriptionResource(resources.ModelResource):
    class Meta:
        model = Prescription

@admin.register(Prescription)
class PrescriptionAdmin(ImportExportModelAdmin):
    resource_class = PrescriptionResource
    list_display = (
        'title', 
        'date'
        )

    search_fields = (
        'title', 
        'beneficiary__beneficiary_id', 
        'service_provider__first_name', 
        'facility__name'
        )

class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service

@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource

    list_display = (
        'title', 
        'client_type', 
        'service_type', 
        'datetime'
        )

class FacilityResource(resources.ModelResource):

    class Meta:
        model = Facility


class BeneficiaryResource(resources.ModelResource):
    class Meta:
        model = Beneficiary

@admin.register(Beneficiary)
class BeneficiaryAdmin(ImportExportModelAdmin):
    resource_class = BeneficiaryResource

    list_display = [
        "beneficiary_id",
        "first_name",
        "last_name",
        "gender", 
        "sex",
        "phone_number",
        "email",
        "date_of_birth",
        "education_level",
    ]
    search_fields = [
        "sex",
        "phone_number",
        "email",
        "beneficiary_id",
        "first_name",
        "last_name",
    ]

class BeneficiaryResource(resources.ModelResource):
    class Meta:
        model = Beneficiary

class BeneficiaryParentAdmin(admin.ModelAdmin):
    list_display = [
        "father_first_name",
        "father_last_name",
        "mother_first_name", 
        "mother_last_name"
    ]

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]


class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ["name", "created"]


class WorkDetailAdmin(admin.ModelAdmin):
    list_display = [
        "gross_pay",
        "company",
        "work_address",
        "insured",
    ]


class AgentDetailAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'birthdate',
        'agent_id',
        'gender',
        'location'
    ]


class FacilityTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]

@admin.register(Facility)
class FacilityAdmin(ImportExportModelAdmin):
    resource_class = FacilityResource
    list_display = ('name', 'province', 'district', 'facility_type', 'hmis_code')

    list_display_links = ('name',)
    search_fields = ('name', 'hmis_code')

    list_filter = ('province', 'facility_type', 'district',)
    list_per_page = 30


class ImplementingPartnerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'ip_type'
    ]
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'qualification',
        'department',
        'facility'
    ]

class ServiceProviderPersonelQualificationAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(ServiceArea, ServiceAreaAdmin)
admin.site.register(AgentDetail, AgentDetailAdmin)
admin.site.register(WorkDetail, WorkDetailAdmin)
admin.site.register(BeneficiaryParent, BeneficiaryParentAdmin)
admin.site.register(FacilityType, FacilityTypeAdmin)
admin.site.register(ImplementingPartner, ImplementingPartnerAdmin)
admin.site.register(ServiceProviderPersonel, ServiceProviderAdmin)
admin.site.register(ServiceProviderPersonelQualification, ServiceProviderPersonelQualificationAdmin)
