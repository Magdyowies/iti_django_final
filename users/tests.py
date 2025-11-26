from django.core import mail
from django.test import TestCase
from django.urls import reverse
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class UserRegistrationTest(TestCase):

    def setUp(self):
        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'mobile_phone': '01012345678',
            'password': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_user_registration(self):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Activate your account', mail.outbox[0].subject)

    def test_user_activation(self):
        self.client.post(reverse('register'), self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        self.assertFalse(user.is_active)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_login_inactive_user(self):
        user = User.objects.create_user(
            email='inactive@example.com',
            password='password',
            is_active=False
        )
        response = self.client.post(reverse('login'), {
            'username': user.email,
            'password': 'password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_active_user(self):
        user = User.objects.create_user(
            email='active@example.com',
            password='password',
            is_active=True
        )
        response = self.client.post(reverse('login'), {
            'username': user.email,
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_invalid_phone_number(self):
        self.user_data['mobile_phone'] = '12345'
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Phone number must be entered in the format: &#x27;+201001234567&#x27;, &#x27;01001234567&#x27;, etc.", response.content.decode())