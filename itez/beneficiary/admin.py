from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from itez.beneficiary.models import (
    Province,
    District,
    ServiceArea,
    WorkDetail,
    Beneficiary,
    BeneficiaryParent
)


class BeneficiaryAdmin(OSMGeoAdmin):
    list_display = [
        "first_name",
        "last_name",
        "beneficiary_code",
        "created",
        "location",
        "parent_details"
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


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(ServiceArea, ServiceAreaAdmin)
admin.site.register(WorkDetail, WorkDetailAdmin)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(BeneficiaryParent)
