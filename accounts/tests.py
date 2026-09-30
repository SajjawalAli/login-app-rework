from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from axes.models import AccessAttempt, AccessLog
from axes.utils import reset

User = get_user_model()


class AuthSystemTests(TestCase):

    def setUp(self):
        # Fully reset django-axes lockout records and state between tests
        reset()
        AccessAttempt.objects.all().delete()
        AccessLog.objects.all().delete()

        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        }

    # Test 1: A new person can sign up
    def test_user_can_signup(self):
        response = self.client.post(self.signup_url, self.valid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    # Test 2: That person can then log in
    def test_user_can_login(self):
        user = User.objects.create_user(
            username='testuserlogin',
            email='login@example.com',
            password='SecurePass123!'
        )
        user.is_active = True
        user.save()

        # Try logging in with username first
        response = self.client.post(self.login_url, {
            'username': 'login@example.com',
            'password': 'SecurePass123!'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    # Test 3: A wrong password is refused
    def test_wrong_password_refused(self):
        user = User.objects.create_user(
            username='testuserwrong',
            email='wrong@example.com',
            password='SecurePass123!'
        )
        user.is_active = True
        user.save()

        response = self.client.post(self.login_url, {
            'username': 'testuserwrong',
            'password': 'WrongPassword123!'
        })
        self.assertEqual(response.status_code, 200)

    # Test 4: A signed-out person cannot reach the profile page
    def test_unauthenticated_user_cannot_access_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)

    # Test 5: The same email cannot be registered twice
    def test_duplicate_email_registration_fails(self):
        User.objects.create_user(
            username='user1',
            email='duplicate@example.com',
            password='SecurePass123!'
        )
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['username'] = 'user2'
        duplicate_data['email'] = 'duplicate@example.com'

        response = self.client.post(self.signup_url, duplicate_data)
        self.assertFormError(
            response.context['form'],
            'email',
            'User with this Email already exists.'
        )