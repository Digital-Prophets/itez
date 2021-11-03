from django.contrib import admin
from itez.beneficiary.models import (
    Province,
    District,
    workDetails
)

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']


class workDetailsAdmin(admin.ModelAdmin):
    list_display = [
        'salary',
        'company',
        'work_address',
        'insured',
    ]

admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(workDetails ,workDetailsAdmin)
