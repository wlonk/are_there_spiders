from django.conf.urls import patterns, url

from .views import CollectionView, InstanceView

urlpatterns = patterns('',
    url(r'^$', CollectionView.as_view(), name='collection'),
    url(r'^(?P<pk>[^/]+)/$', InstanceView.as_view(), name='instance'),
)
