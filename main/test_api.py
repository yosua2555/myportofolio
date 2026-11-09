import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from main.models import Project, Education

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password"
        )
        self.project = Project.objects.create(
            name="Portfolio", description="My website", date=2026
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "name": "New project",
            "description": "A useful app",
            "date": 2026,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"name": "Port"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"name": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"name": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"name": " "}, "name"),
            ({"name": '<img src="x" onerror="alert(1)">'}, "name"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"name": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Changed")

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_edu", password="test-password", email="owner_edu@example.com"
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(
            username="editor_edu", password="test-password"
        )
        self.editor.groups.add(self.editor_group)

        self.visitor = User.objects.create_user(
            username="visitor_edu", password="test-password"
        )
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            description="Fasilkom UI",
            started_year=2025,
            ended_year=2029,
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.star_url = reverse("api:education-star", args=[self.education.id])
        self.payload = {
            "institution": "SMA Negeri 1",
            "degree": "MIPA",
            "description": "Jurusan IPA",
            "started_year": 2021,
            "ended_year": 2024,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.education.id))
        self.assertEqual(response.data[0]["institution"], "Universitas Indonesia")
        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(response.data[0]["star_count"], 0)
        self.assertNotIn("fields", response.data[0])

        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data["id"], str(self.education.id))

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"institution": "Indonesia"})
        self.assertEqual(len(response.data), 1)

        response = self.client.get(self.list_url, {"institution": "TidakAda"})
        self.assertEqual(response.data, [])

    def test_missing_education(self):
        url = reverse("api:education-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            # Create (POST) ditolak
            post_res = self.client.post(self.list_url, self.payload, format="json")
            self.assertEqual(post_res.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(Education.objects.count(), 1)

            # Update (PATCH & PUT) ditolak
            patch_res = self.client.patch(self.detail_url, {"degree": "Hacked"}, format="json")
            self.assertEqual(patch_res.status_code, status.HTTP_403_FORBIDDEN)
            self.education.refresh_from_db()
            self.assertEqual(self.education.degree, "S1 Sistem Informasi")

            put_res = self.client.put(self.detail_url, self.payload, format="json")
            self.assertEqual(put_res.status_code, status.HTTP_403_FORBIDDEN)

            # Delete (DELETE) ditolak
            del_res = self.client.delete(self.detail_url)
            self.assertEqual(del_res.status_code, status.HTTP_403_FORBIDDEN)
            self.assertTrue(Education.objects.filter(pk=self.education.id).exists())

    def test_editor_permissions(self):
        self.client.force_authenticate(user=self.editor)

        # Editor ditolak membuat data (POST)
        post_res = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(post_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)

        # Editor ditolak menghapus data (DELETE)
        del_res = self.client.delete(self.detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Education.objects.filter(pk=self.education.id).exists())

        # Editor diizinkan mengubah data (PATCH)
        patch_res = self.client.patch(self.detail_url, {"degree": "S1 Ilmu Komputer"}, format="json")
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Ilmu Komputer")

        # Editor diizinkan mengubah data (PUT)
        updated_payload = {
            "institution": "Universitas Indonesia",
            "degree": "S1 Sistem Informasi Unggulan",
            "description": "Fasilkom UI Terbaik",
            "started_year": 2025,
            "ended_year": 2029,
        }
        put_res = self.client.put(self.detail_url, updated_payload, format="json")
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Sistem Informasi Unggulan")

    def test_owner_permissions(self):
        self.client.force_authenticate(user=self.owner)

        # Owner dapat membuat data (POST)
        post_res = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        new_id = post_res.data["id"]
        self.assertTrue(Education.objects.filter(pk=new_id).exists())

        # Owner dapat mengedit (PATCH)
        patch_res = self.client.patch(self.detail_url, {"institution": "UI Salemba"}, format="json")
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "UI Salemba")

        # Owner dapat menghapus (DELETE)
        del_res = self.client.delete(self.detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(pk=self.education.id).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)

        # Validasi kosong
        for bad_payload, field in [
            ({**self.payload, "institution": "  "}, "institution"),
            ({**self.payload, "degree": ""}, "degree"),
        ]:
            res = self.client.post(self.list_url, bad_payload, format="json")
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, res.data)

        # Validasi sanitasi XSS (strip_tags)
        xss_payload = {
            **self.payload,
            "institution": '<b>UI</b><script>alert(1)</script>',
            "degree": '<i>Degree</i>',
            "description": '<p>Description</p>',
        }
        res = self.client.post(self.list_url, xss_payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_obj = Education.objects.get(pk=res.data["id"])
        self.assertEqual(created_obj.institution, "UIalert(1)")
        self.assertEqual(created_obj.degree, "Degree")
        self.assertEqual(created_obj.description, "Description")

    def test_star_requires_login_and_toggles(self):
        # Pengunjung tanpa login ditolak memberi star
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)

        # Pengguna biasa login dapat memberi star
        self.client.force_authenticate(user=self.visitor)
        star_res = self.client.post(self.star_url)
        self.assertEqual(star_res.status_code, status.HTTP_200_OK)
        self.assertTrue(star_res.data["is_starred"])
        self.assertEqual(star_res.data["star_count"], 1)
        self.assertTrue(self.education.starred_by.filter(pk=self.visitor.pk).exists())

        # Pengguna biasa membatalkan star (unstar)
        unstar_res = self.client.post(self.star_url)
        self.assertEqual(unstar_res.status_code, status.HTTP_200_OK)
        self.assertFalse(unstar_res.data["is_starred"])
        self.assertEqual(unstar_res.data["star_count"], 0)
        self.assertFalse(self.education.starred_by.filter(pk=self.visitor.pk).exists())

    def test_csrf_protection_enforced(self):
        # Menggunakan client dengan enforce_csrf_checks=True dan .login()
        csrf_client = APIClient(enforce_csrf_checks=True)
        logged_in = csrf_client.login(username="owner_edu", password="test-password")
        self.assertTrue(logged_in)

        # Request POST tanpa token CSRF harus ditolak 403 Forbidden
        response = csrf_client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Pastikan tidak ada data baru tersimpan di database
        self.assertEqual(Education.objects.count(), 1)
