import json
from multiprocessing import managers
from threading import local
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    args = "<filename>"
    help = "Loads the initial data in to database"

    def handle(self, *args, **options):
        
        call_command("loaddata", "itez/fixtures/users.json", verbosity=0)
        
        print("--------- DATA WAS LOADED SUCCESSFULLY ---------")

       
