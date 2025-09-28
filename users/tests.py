from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Profile should be automatically created by the signal
        self.profile = self.user.profile
        
        # Update profile with test data
        self.profile.phone_number = '123-456-7890'
        self.profile.address = '123 Test St'
        self.profile.city = 'Test City'
        self.profile.postal_code = '12345'
        self.profile.save()
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone_number, '123-456-7890')
        self.assertEqual(self.profile.address, '123 Test St')
        self.assertEqual(self.profile.city, 'Test City')
        self.assertEqual(self.profile.postal_code, '12345')
    
    def test_profile_str_representation(self):
        self.assertEqual(str(self.profile), "testuser's profile")
    
    def test_profile_signal_creation(self):
        # Create a new user and check if profile is automatically created
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpassword'
        )
        
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertIsNotNone(new_user.profile)

class UserFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_registration_form_valid_data(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_registration_form_invalid_data(self):
        # Test with mismatched passwords
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': 'complex_password123',
            'password2': 'different_password'
        }
        
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_user_update_form(self):
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_profile_update_form(self):
        form_data = {
            'phone_number': '987-654-3210',
            'address': '456 New St',
            'city': 'New City',
            'postal_code': '54321'
        }
        
        form = ProfileUpdateForm(data=form_data, instance=self.user.profile)
        self.assertTrue(form.is_valid())

class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
    
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
    
    def test_register_view_post(self):
        user_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        
        response = self.client.post(reverse('register'), user_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
        # Check if user was created
        new_user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, 'new@example.com')
    
    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
    
    def test_profile_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        
        profile_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'phone_number': '987-654-3210',
            'address': '456 New St',
            'city': 'New City',
            'postal_code': '54321'
        }
        
        response = self.client.post(reverse('profile'), profile_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Refresh user from database
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        
        # Check if user and profile were updated
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.phone_number, '987-654-3210')
        self.assertEqual(self.user.profile.city, 'New City')