import os
import django

# Set the environment variable for Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookMyFlight.settings')  # Adjust to your settings module

# Initialize Django
django.setup()

from Flight.models import Week 

def createWeekDays():
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for i,day in enumerate(days):
        Week.objects.create(number=i, name=day)


try: 
    if(len(Week.objects.all()) == 0): 
        createWeekDays()
    else: 
        print("Added week data already.")
except: 
    pass