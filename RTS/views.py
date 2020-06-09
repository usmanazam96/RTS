from django.http import HttpResponse

from django.shortcuts import render
from faculty.models import FacultyAvailability
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    faculty_availability = FacultyAvailability.objects.all().order_by('-availability')
    page = request.GET.get('page', 1)

    paginator = Paginator(faculty_availability, 10)
    try:
        faculty_availability = paginator.page(page)
    except PageNotAnInteger:
        faculty_availability = paginator.page(1)
    except EmptyPage:
        faculty_availability = paginator.page(paginator.num_pages)
    context = dict(page_title='Home', h1_title='Home', url='home', faculty_availability=faculty_availability)
    return render(request, 'RTS/index.html', context)
