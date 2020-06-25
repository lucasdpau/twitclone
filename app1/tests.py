from django.test import TestCase, SimpleTestCase, Client
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

class SettingsTests(TestCase):
	def setUp(self):
		User.objects.create_user('test', 'test1@test.com', 'q')
		
	def test_login_works(self):
	#login works
		c = Client()
		is_logged_in = c.login(username='test', password='q')
		self.assertEquals(is_logged_in, True)

	def test_default_page(self):
	#test that if we set default page to yourfeed, we get that page when we log in
		test_user = User.objects.get(username='test')
		test_profile = Profile.objects.get(user__username=test_user.username)
		test_profile.default_page = "yourfeed"
		test_profile.save()
		c = Client()
		response = c.post('/login', {"username":"test", "password":"q"} , follow=True)
		self.assertContains(response, "<title>Your Feed</title>")

	def test_default_page_is_all(self):
	#test that by default the user redirects to all posts after login
		c = Client()
		response = c.post('/login', {"username":"test", "password":"q"} , follow=True)
		self.assertNotContains(response, "<title>Your Feed</title>")

class YourFeedTests(TestCase):
	def setUp(self):
		User.objects.create_user('test1', 'test1@test.com', 'q')
		followed_user = User.objects.create_user('followed_user', 'follow@test.com', 'q')
		unfollowed_user = User.objects.create_user('unfollowed_user', 'unfollow@test.com', 'q')
		followed_tweet = Tweet(text="tweet by followed", author=followed_user)
		followed_tweet.save()
		unfollowed_tweet = Tweet(text="you shouldn't see this", author=unfollowed_user)
		unfollowed_tweet.save()

	
	def test_follow(self):
		test_user = User.objects.get(username='test1')
		test_profile = Profile.objects.get(user__username=test_user.username)
		followed_user = User.objects.get(username='followed_user')
		followed_user_profile = Profile.objects.get(user__username=followed_user.username)
		test_profile.following.add(followed_user_profile)
		self.assertIn(followed_user_profile, Profile.objects.filter(followed_by=test_profile))

	def test_followed_user_in_feed(self):
# add followed users, but not the unfollowed one, see if followed user is in profile.following
		test_user = User.objects.get(username='test1')
		test_profile = Profile.objects.get(user__username=test_user.username)
		followed_user = User.objects.get(username='followed_user')
		followed_user_profile = Profile.objects.get(user__username=followed_user.username)
		test_profile.following.add(followed_user_profile)
		
		followed_user_tweet = Tweet.objects.get(author=followed_user)
		tweet_list = []
		for items in Tweet.objects.all():
			if items.author.profile in test_profile.following.all():
				tweet_list.append(items)
		self.assertIn(followed_user_tweet , tweet_list)

	def test_unfollowed_user_not_in_feed(self):
# add followed users, but not the unfollowed one
		test_user = User.objects.get(username='test1')
		test_profile = Profile.objects.get(user__username=test_user.username)
		followed_user = User.objects.get(username='followed_user')
		followed_user_profile = Profile.objects.get(user__username=followed_user.username)
		test_profile.following.add(followed_user_profile)
		unfollowed_user = User.objects.get(username='unfollowed_user')

		unfollowed_user_tweet = Tweet.objects.get(author=unfollowed_user)
		tweet_list = []
		for items in Tweet.objects.all():
			if items.author.profile in test_profile.following.all():
				tweet_list.append(items)
		self.assertNotIn(unfollowed_user_tweet , tweet_list)
