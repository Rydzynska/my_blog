from django import template
from ..models import Post, Tag, Category
from django.db.models import Count


from django.utils import timezone

register = template.Library()


@register.inclusion_tag('blog/post_history.html')
def post_history():
    posts = Post.objects.order_by(
        '-published_date').filter(published_date__lte=timezone.now())[:5]
    return {'posts': posts}

@register.inclusion_tag('blog/tag_cloud.html')
def tag_cloud():
    tags = Tag.objects.filter(
            post__published_date__lte=timezone.now()).order_by("tag").annotate(
            post_count=Count('post'))
    return {'tags': tags}

@register.inclusion_tag('blog/category.html')
def category():
    categories = Category.objects.filter(
            post__published_date__lte=timezone.now()).annotate(
            post_count=Count('post'))
    return {'categories': categories}