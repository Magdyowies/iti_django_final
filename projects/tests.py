from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from .models import Project
from users.models import User
from django.core.exceptions import ValidationError

class ProjectModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')

    def test_end_date_before_start_date(self):
        project = Project(
            owner=self.user,
            title='Test Project',
            details='Test Details',
            target_amount=1000,
            start_date=date.today(),
            end_date=date.today() - timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

class ProjectViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='owner@example.com', password='password')
        self.other_user = User.objects.create_user(email='other@example.com', password='password')
        self.project = Project.objects.create(
            owner=self.user,
            title='Test Project',
            details='Test Details',
            target_amount=1000,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
        )

    def test_owner_can_edit_project(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('project-update', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_edit_project(self):
        self.client.login(email='other@example.com', password='password')
        response = self.client.get(reverse('project-update', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_owner_can_delete_project(self):
        self.client.login(email='owner@example.com', password='password')
        response = self.client.get(reverse('project-delete', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_delete_project(self):
        self.client.login(email='other@example.com', password='password')
        response = self.client.get(reverse('project-delete', kwargs={'pk': self.project.pk}))
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_search_by_date(self):
        response = self.client.get(reverse('project-list'), {'date': date.today().strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)

        response = self.client.get(reverse('project-list'), {'date': (date.today() + timedelta(days=20)).strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.project.title)