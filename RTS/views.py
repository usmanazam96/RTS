from django.http import HttpResponse

from django.shortcuts import render
from faculty.models import FacultyAvailability


# Create your views here.
def index(request):
    faculty_availability = FacultyAvailability.objects.all()
    context = dict(page_title='Home', h1_title='Home', url='home', faculty_availability=faculty_availability)
    return render(request, 'RTS/index.html', context)
