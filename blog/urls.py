from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.AboutView.as_view(), name='about_view'),
	url(r'^tag/(?P<slug>[-\w]*)/$', views.TagIndexView.as_view(), name='tagged'),
    url(r'^category/(?P<slug>[-\w]*)/$', views.CategoryIndexView.as_view(), name='category_view'),
	url(r'^(?P<slug>[-\w]*)/$', views.PostDetail.as_view(), name='post_detail'),
	]