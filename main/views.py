import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

# Import model & form yang dibutuhkan
from main.models import Experience, Education, Project
from main.forms import EducationForm, ProjectForm


# Helper function untuk mengecek apakah user adalah Editor atau Superuser
def is_editor_or_superuser(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Editor').exists())


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    
    context = {
        "name": "Yosua Peitho Purba",
        "npm": "2506657402",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Student @ Universitas Indonesia | Software "
            "Development and Cyber Security Enthusiast"
        ),
        "last_login": last_login,
        "form": ProjectForm(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Yosua Peitho Purba",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


# ==========================================
# EDUCATION SECTION (Tugas 3, 4, & 5)
# ==========================================

def show_education(request):
    is_editor = is_editor_or_superuser(request.user)

    context = {
        "name": "Yosua Peitho Purba",
        "institution_query": request.GET.get("institution", "").strip(),
        "is_editor": is_editor,
        "form": EducationForm(),  # Form kosong untuk Modal Tambah Education (Tugas 5)
    }
    return render(request, "education.html", context)


def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()
    education_list = Education.objects.all()
    
    if institution_query:
        education_list = education_list.filter(institution__icontains=institution_query)
        
    data = []
    for edu in education_list:
        data.append({
            "pk": str(edu.id),
            "fields": {
                "institution": edu.institution,
                "degree": edu.degree,
                "description": edu.description,
                "started_year": edu.started_year,
                "ended_year": edu.ended_year or "Present",
            }
        })
    return JsonResponse(data, safe=False)


def get_education_xml(request):
    institution_query = request.GET.get("institution", "").strip()
    education_list = Education.objects.all()
    
    if institution_query:
        education_list = education_list.filter(institution__icontains=institution_query)
        
    education_xml = serializers.serialize("xml", education_list)
    return HttpResponse(education_xml, content_type="application/xml")


@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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


@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya superuser yang dapat menambahkan data pendidikan."},
            status=403,
        )
        
    form = EducationForm(request.POST)
    if form.is_valid():
        edu = form.save()
        return JsonResponse(
            {"message": "Data pendidikan berhasil ditambahkan.", "pk": str(edu.id)},
            status=201,
        )
        
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def update_education(request, education_id):
    if not is_editor_or_superuser(request.user):
        raise PermissionDenied

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


@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Riwayat pendidikan berhasil dihapus!")
        return redirect("main:show_education")
    return redirect("main:show_education")


# ==========================================
# PROJECT SECTION
# ==========================================

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:show_main")

    context = {"form": form}
    return render(request, "project_form.html", context)


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )
        
    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )
        
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


def get_projects_json(request):
    name_query = request.GET.get("name", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()
    
    if name_query:
        projects = projects.filter(name__icontains=name_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users]) if starred_users else "Belum ada"

        data.append({
            "pk": str(project.id),
            "fields": {
                "name": project.name,
                "date": project.date,
                "description": project.description,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
        
    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
            
    return redirect("main:show_main")


# ==========================================
# AUTHENTICATION SECTION
# ==========================================

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
        
    context = {
        "name": "Yosua Peitho Purba",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response
        
    context = {
        "name": "Yosua Peitho Purba",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response