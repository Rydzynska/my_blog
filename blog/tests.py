from django.test import TestCase
from .models import Post, Comment, Tag, Category
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
import datetime
from django.utils import timezone
from .forms import CommentForm
from django_webtest import WebTest
from django.template import Template, Context


class PostModelTest(TestCase):

	def test_string_representation(self):
		category = Category.objects.create(name='1-category')
		post = Post.objects.create(title="My entry title", intro='1-intro', published_date=timezone.now(), category=category )
		self.assertEqual(str(post), post.title)

	def test_get_absolute_url(self):
		category = Category.objects.create(name='1-category')
		post = Post.objects.create(title="My entry title", intro='1-intro', published_date=timezone.now(), category=category )
		self.assertIsNotNone(post.get_absolute_url())

class ViewsTests(TestCase):

	def test_homepage(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

class HomePageTests(TestCase):

	def test_one_entry(self):
		time = timezone.now() - datetime.timedelta(days=5)
		category = Category.objects.create(name='1-category')
		Post.objects.create(title='1-title', intro='1-intro', published_date=time, category=category)
		response = self.client.get('/')
		self.assertContains(response, '1-title')
		self.assertContains(response, '1-intro')

	def test_two_entries(self):
		time = timezone.now() - datetime.timedelta(days=5)
		category = Category.objects.create(name='1-category')
		Post.objects.create(title='1-title', intro='1-intro', published_date=time, category=category)
		time = timezone.now() - datetime.timedelta(days=3)
		Post.objects.create(title='2-title', intro='2-intro', published_date=time, category=category)
		response = self.client.get('/')
		self.assertContains(response, '1-title')
		self.assertContains(response, '1-intro')
		self.assertContains(response, '2-title')

	def test_no_posts(self):
		response = self.client.get('/')
		self.assertContains(response, 'No blog posts added.')

class PostViewTest(WebTest):

	def setUp(self):
		self.category = Category.objects.create(name='1-category')
		self.post = Post.objects.create(title='1-title', intro='1-intro', category=self.category)

	def test_basic_view(self):
		response = self.client.get(self.post.get_absolute_url())
		self.assertEqual(response.status_code, 200)

	def test_index_view_with_a_past_post(self):
		time = timezone.now() + datetime.timedelta(days=-30)
		category = Category.objects.create(name='1-category')
		Post.objects.create(title='Past post', intro='1-intro', published_date=time, category=category)
		response = self.client.get('/')
		self.assertContains(response, 'Past post')

	def test_index_view_with_a_future_post(self):
		time = timezone.now() + datetime.timedelta(days=30)
		category = Category.objects.create(name='1-category')
		Post.objects.create(title='Future post', intro='1-intro', published_date=time, category=category)
		response = self.client.get('/')
		self.assertContains(response, "No blog posts added.",
                            status_code=200)
        
	def test_index_view_with_future_post_and_past_post(self):
		time = timezone.now() + datetime.timedelta(days=30)
		category = Category.objects.create(name='1-category')
		future_post = Post.objects.create(title='Future post', intro='1-intro', published_date=time, category=category)
		time = timezone.now() + datetime.timedelta(days=-30)
		past_post = Post.objects.create(title='Past post', intro='1-intro', published_date=time, category=category)
		response = self.client.get('/')
		self.assertEqual(str(past_post), 'Past post')

	def test_url(self):
		title = "This is my test title"
		today = datetime.date.today()
		category = Category.objects.create(name='1-category')
		post = Post.objects.create(title=title, intro="Some intro", published_date=today, category=category)
		slug = slugify(title)
		url = "/{slug}/".format(
			slug=slug,
		)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, template_name='blog/post_detail.html')

	def test_invalid_url(self):
		today = datetime.date.today()
		category = Category.objects.create(name='1-category')
		post = Post.objects.create(title="title", intro="intro", published_date=today, category=category)
		response = self.client.get("invalid/")
		self.assertEqual(response.status_code, 404)

	def test_no_comments(self):
		response = self.client.get('/')
		self.assertContains(response, 'No blog posts added.')

	def test_view_page(self):
		page = self.app.get(self.post.get_absolute_url())
		self.assertEqual(len(page.forms), 1)

	def test_form_error(self):
		page = self.app.get(self.post.get_absolute_url())
		page = page.form.submit()
		self.assertContains(page, 'Please enter your name')

	def test_form_success(self):
		page = self.app.get(self.post.get_absolute_url())
		page.form['name'] = 'Tom'
		page.form['email'] = 'tom@example.com'
		page.form['comment'] = 'Test comment body.'
		page = page.form.submit()
		self.assertRedirects(page, self.post.get_absolute_url())	

class CommentModelTest(TestCase):

	def test_string_representation(self):
		comment = Comment(comment="My comment body")
		self.assertEqual(str(comment), "My comment body")

	def test_gravatar_url(self):
		comment = Comment(name='Tom', comment="My comment body", email="tom@example.com")
		expected = "http://www.gravatar.com/avatar/e4f7cd8905e896b04425b1d08411e9fb?d=identicon&s=50"
		self.assertEqual(comment.gravatar_url(), expected)

class CommentFormTest(TestCase):

	def setUp(self):
		time = timezone.now()
		self.category = Category.objects.create(name='1-category')
		self.post = Post.objects.create(title='1-title', intro='1-intro', published_date=time, category=self.category)

	def test_init(self):
		CommentForm(post=self.post)

	def test_init_without_entry(self):
		with self.assertRaises(KeyError):
			CommentForm()

	def test_valid_data(self):
		form = CommentForm({
			'name': 'Tom Hanks',
			'email': 'tom@example.com',
			'comment': 'Hello there',
		}, post=self.post)
		self.assertTrue(form.is_valid())
		comment = form.save()
		self.assertEqual(comment.name, 'Tom Hanks')
		self.assertEqual(comment.email, 'tom@example.com')
		self.assertEqual(comment.comment, 'Hello there')
		self.assertEqual(comment.post, self.post)

	def test_blank_data(self):
		form = CommentForm({}, post=self.post)
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors, {
			'name': ['Please enter your name'],
			'email': ['Please enter your e-mail address'],
			'comment': ['Please enter your comment'],
		})

class TagModelTest(TestCase):

    def test_string_representation(self):
        tag = Tag(tag="django")
        self.assertEqual(str(tag), "django")

    def test_tag_for_future_post(self):
        time = timezone.now() + datetime.timedelta(days=30)
        category = Category.objects.create(name='1-category')
        future_post = Post.objects.create(title='Future post', intro='1-intro', published_date=time, 
        	category=category)
        tag = Tag(tag='1-tag')
        tag.save()
        future_post.save()
        future_post.tags.add(tag)
        response = self.client.get('/')
        self.assertContains(response, 'No tags added.')

class PostHistoryTagTest(TestCase):

	TEMPLATE = Template("{% load blog_tags %} {% post_history %}")

	def test_post_shows_up(self):
		category = Category.objects.create(name='1-category')
		post = Post.objects.create(title='My post title', intro='My intro', published_date=timezone.now(), category=category)
		rendered = self.TEMPLATE.render(Context({}))
		self.assertIn(post.title, rendered)

	def test_no_posts(self):
		rendered = self.TEMPLATE.render(Context({}))
		self.assertIn("No recent posts.", rendered)

	def test_many_posts(self):
		category = Category.objects.create(name='1-category')
		for n in range(6):
			Post.objects.create(title="Post #{0}".format(n), intro='My intro', published_date=timezone.now(),
				category=category)
		rendered = self.TEMPLATE.render(Context({}))
		self.assertIn("Post #5", rendered)
		self.assertNotIn("Post #6", rendered)

