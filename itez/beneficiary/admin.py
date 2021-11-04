from django.contrib import admin
from itez.beneficiary.models import (
    Province,
    District,
    WorkDetail,
    AgentDetail
)

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

class WorkDetailAdmin(admin.ModelAdmin):
    list_display = [
        'gross_pay',
        'company',
        'work_address',
        'insured',
    ]

class AgentDetailAdmin(admin.ModelAdmin):
    list_display = [
        'role',
        'first_name',
        'second_name',
        'birthdate',
        'agend_id',
        'gender',
        'assigned_location'
    ]

admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(WorkDetail ,WorkDetailAdmin)
admin.site.register(AgentDetail, AgentDetailAdmin)
