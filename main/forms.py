from django.forms import ModelForm, TextInput, Textarea, NumberInput
from main.models import Education

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