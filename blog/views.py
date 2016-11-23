from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import CreateView
from django.views.generic import ListView, DetailView, TemplateView
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.db.models import Count
from django.template.loader import get_template
from django.template import Context 
from django.contrib import messages

import logging

from .forms import CommentForm
from .forms import ContactForm
from .models import Post, Comment, Tag

class TagIndexView(ListView):
    template_name = 'blog/selected_view.html'
    model = Post
    paginate_by = '5'

    def get_queryset(self):
        return Post.objects.select_related().annotate(
        comment_count=Count('comment')).order_by(
        '-published_date').filter(
        tags__slug=self.kwargs.get('slug')).filter(
        published_date__lte=timezone.now())

class HomeView(ListView):
    template_name = 'blog/index.html'
    paginate_by = '5'

    def get_queryset(self):
    	return Post.objects.select_related().annotate(
    	comment_count=Count('comment')).order_by(
    	'-published_date').filter(published_date__lte=timezone.now())

class PostDetail(CreateView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['post'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['post'] = self.get_object()
        return d

    def get_success_url(self):
        return self.get_object().get_absolute_url()

class CategoryIndexView(ListView):
    template_name = 'blog/selected_view.html'
    model = Post
    paginate_by = '3'

    def get_queryset(self):
        return Post.objects.select_related().annotate(
        comment_count=Count('comment')).order_by(
        '-published_date').filter(
        category__slug=self.kwargs.get('slug')).filter(
        published_date__lte=timezone.now())

class AboutView(TemplateView):
    template_name = 'blog/about.html'

logger = logging.getLogger(__name__)

def myfunction():
    logger.debug("this is a debug message!")

def myotherfunction():
    logger.error("this is an error message!!")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name', '')
            contact_email = request.POST.get(
                'contact_email', '')
            form_content = request.POST.get(
                'content', '')

            template = get_template('blog/contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })

            content = template.render(context)

            email = EmailMessage(
                'Learning Freak form submission',
                content,
                'no-reply',
                ['rydzynska.agnieszka@gmail.com'],
                headers = {'Reply-To': contact_email }
                )
            email.send(fail_silently=False)

            messages.success(request, 'Message was sent succesfully. Thanks!')

            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form, })