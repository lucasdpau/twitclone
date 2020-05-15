from django.test import TestCase
from django.contrib.auth.models import User
from .models import Tweet, Profile, Tags

# Create your tests here.

class UserTestCase(TestCase):
	def setup(self):
		User.objects.create_user('test', 'test@test.com', 'q')

	def teardown(self):
		User.objects.get(username='test').delete()

class ProfileTestCase(TestCase):
	def setup(self):
		User.objects.create_user('test1', 'test1@test.com', 'q')
		test_user = User.objects.get(username='test1')
		test_profile = Profile(user=test_user)
		test_profile.save()

	def teardown(self):
		User.objects.get(username='test1').delete()

class TweetTestCase(TestCase):
	def setup(self):
		Tweet.objects.create(text="testing 123 #abc",)