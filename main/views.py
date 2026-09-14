from django.shortcuts import render
from main.models import Experience, Education 

def show_main(request):
    context = {
        "name": "Yosua Peitho Purba",
        "npm": "2506657402",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Student @ Universitas Indonesia | Software "
            "Development and Cyber Security Enthusiast"
        ),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Yosua Peitho Purba",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    education_list = Education.objects.all()
    context = {
        'name': 'Yosua Peitho Purba',
        'education_list': education_list,
    }
    return render(request, 'education.html', context)