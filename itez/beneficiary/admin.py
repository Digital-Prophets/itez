from django.contrib import admin
from itez.beneficiary.models import (
    Province,
    District,
    ServiceArea,
    WorkDetail,
    AgentDetail,
    Beneficiary,
    BeneficiaryParent,
    Appointment
)


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "beneficiary_ID",
        "created",
        "parent_details",
        "agent_ID"
    ]


class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "facility_name",
        "department_name",
        "start_time",
        "end_time",
        "created_at",
        "beneficiary"
    ]


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
        'gender',
        'location'
    ]

admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(ServiceArea, ServiceAreaAdmin)
admin.site.register(AgentDetail, AgentDetailAdmin)
admin.site.register(WorkDetail, WorkDetailAdmin)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(BeneficiaryParent, BeneficiaryParentAdmin)
admin.site.register(Appointment, AppointmentAdmin)
