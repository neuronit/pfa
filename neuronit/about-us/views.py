from django.shortcuts import render
from .models import *


def about_us(request):

    par_list = DescriptionP.objects.all()
    team_list = TeamMember.objects.all()
    
    context = {
        'par_list' : par_list,
        'team_list' : team_list,
    }

    return render(request, 'about-us/about-us.html', context)
