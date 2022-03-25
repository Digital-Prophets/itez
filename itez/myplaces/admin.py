from django.contrib.gis import admin

from leaflet.admin import LeafletGeoAdmin

from .models import Agent, MedicalRecord, Myplaces,Beneficiary

admin.site.register(Beneficiary)
admin.site.register(Agent)
admin.site.register(MedicalRecord)
@admin.register(Myplaces)


class MyplacesAdmin(LeafletGeoAdmin):

    list_display = ('name', 'location')