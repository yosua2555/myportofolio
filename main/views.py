from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from main.models import Experience, Education
from main.forms import EducationForm
from main.views import ProjectForm

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
    # Mengambil data dari JSON response lalu di-deserialize
    json_response = get_education_json(request)
    education_objects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [item.object for item in education_objects]
    institution_query = request.GET.get("institution", "").strip()

    context = {
        "name": "Yosua Peitho Purba",
        "education_list": education_list,
        "institution_query": institution_query,
    }
    return render(request, "education.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Yosua Peitho Purba",
        "form": form,
    }
    return render(request, "education_form.html", context)

def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()
    education_list = Education.objects.all()
    
    if institution_query:
        education_list = education_list.filter(institution__icontains=institution_query)
        
    education_json = serializers.serialize("json", education_list)
    return HttpResponse(education_json, content_type="application/json")

def get_education_xml(request):
    institution_query = request.GET.get("institution", "").strip()
    education_list = Education.objects.all()
    
    if institution_query:
        education_list = education_list.filter(institution__icontains=institution_query)
        
    education_xml = serializers.serialize("xml", education_list)
    return HttpResponse(education_xml, content_type="application/xml")

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")
    return redirect("main:show_education")

def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat pendidikan berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Yosua Peitho Purba",
        "form": form,
    }
    return render(request, "education_form.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:show main")

    context = {"form" : form}
    return render(request, "project_form.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
        
    context = {
        "name": "Yosua",  # Sesuaikan dengan nama kamu
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("main:show_main")
        
    context = {
        "name": "Yosua",  # Sesuaikan dengan nama kamu
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return redirect("main:show_main")
