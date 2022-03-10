import json
from multiprocessing import managers
from threading import local
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    args = "<filename>"
    help = "Loads the initial data in to database"

    def handle(self, *args, **options):
        
        call_command("loaddata", "itez/fixtures/province.json", verbosity=0)
        call_command("loaddata", "itez/fixtures/district.json", verbosity=0)
        call_command("loaddata", "itez/fixtures/facility_type.json", verbosity=0)
        call_command("loaddata", "itez/fixtures/facility.json", verbosity=0)
        call_command("loaddata", "itez/fixtures/beneficiary.json", verbosity=0)
        call_command("loaddata", "itez/fixtures/agents.json", verbosity=0)
        call_command("loaddata", "itez/fixtures/services.json", verbosity=0)
        call_command("loaddata", "itez/fixtures/medical_records.json", verbosity=0)

        print("--------- SAMPLE DATA WAS LOADED SUCCESSFULLY ---------")

       
