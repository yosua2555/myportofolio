from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, NumberInput
from django.utils.html import strip_tags
from main.models import Education, Project


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "description",
            "started_year",
            "ended_year",
        ]
        labels = {
            "institution": "Nama Instansi / Universitas",
            "degree": "Gelar / Program",
            "description": "Deskripsi",
            "started_year": "Tahun Mulai",
            "ended_year": "Tahun Selesai (Opsional)",
        }
        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "degree": TextInput(
                attrs={
                    "placeholder": "S1 Sistem Informasi",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsikan kegiatan akademik atau prestasi selama studi...",
                    "rows": 3,
                }
            ),
            "started_year": NumberInput(
                attrs={
                    "placeholder": "2025",
                }
            ),
            "ended_year": NumberInput(
                attrs={
                    "placeholder": "2029 (Biarkan kosong jika masih berlangsung)",
                }
            ),
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "date", "description"]
        labels = {
            "name": "Nama Proyek",
            "date": "Tahun Dibuat",
            "description": "Deskripsi Proyek",
        }
        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Contoh: Website Portofolio Django",
                    "maxlength": 255,
                }
            ),
            "date": NumberInput(
                attrs={
                    "placeholder": "2026",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan teknologi dan fitur utama proyek...",
                    "rows": 3,
                }
            ),
        }

    # DITAMBAHKAN: Method validasi & pembersihan XSS di server
    def clean_name(self):
        name = strip_tags(self.cleaned_data["name"]).strip()
        if not name:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return name

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi proyek tidak boleh hanya berisi tag HTML.")
        return description