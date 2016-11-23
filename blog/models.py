from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone
import hashlib

class Tag(models.Model):
    tag = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(default='', editable=False)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        kwargs = {'slug': self.slug}
        return reverse('tagged', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag)
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(default='', max_length=100, blank=True, null=True)
    slug = models.SlugField(default='', editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        kwargs = {'slug': self.slug}
        return reverse('category_view', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Post(models.Model):	
    title = models.CharField(max_length=500)
    intro = models.TextField()
    text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True) 
    slug = models.SlugField(default='', editable=False)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'slug': self.slug}
        return reverse('post_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment

    def gravatar_url(self):
        email = self.email.replace(" ", "").lower()
        md5 = hashlib.md5(email.encode())
        digest = md5.hexdigest() + '?d=identicon&s=50'

        return 'http://www.gravatar.com/avatar/{}'.format(digest)
