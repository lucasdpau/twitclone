from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from .models import Tweet, Profile, Tags

# Create your tests here.

class UserTestCase(TestCase):
	#setUp will run before each test, although variable names will not transfer over
	def setUp(self):
		User.objects.create_user('test', 'test@test.com', 'q')

	def test_user_created(self):
		user = User.objects.get(username='test')
		self.assertEqual(user.email, 'test@test.com')

	def teardown(self):
		User.objects.get(username='test').delete()

class ProfileTestCase(TestCase):
	def setUp(self):
		User.objects.create_user('test1', 'test1@test.com', 'q')
		test_user = User.objects.get(username='test1')
		test_profile = Profile(user=test_user)

	def test_user_created_properly(self):
		test_user = User.objects.get(username='test1')
		self.assertEqual(test_user.email, 'test1@test.com')

	def test_profile_attached_to_user(self):
		test_profile = Profile.objects.get(user__username='test1')
		self.assertEqual(test_profile.user.email, 'test1@test.com')
		self.assertEqual(test_profile.user.username, 'test1')	

	def teardown(self):
		User.objects.get(username='test1').delete()

class TweetTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user('test', 'test@test.com', 'q')
		user.save()
		Tweet.objects.create(text="testing 123 #abc", author=user)
		Tweet.save()

	def teardown(self):
		Tweet.objects.get(text="testing 123 #abc").delete()

class MainPageTests(SimpleTestCase):
	def test_home_page_status_code(self):
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)

	def test_home_page_status_post(self):
		response = self.client.post('/')
		self.assertEquals(response.status_code, 200)