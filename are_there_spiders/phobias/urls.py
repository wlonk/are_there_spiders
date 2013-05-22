from django.conf.urls import patterns, url

from .views import (
    CollectionView,
    CreateView,
    ArtworkInstanceView,
    EditView,
    DeleteView
)

urlpatterns = patterns('',
    url(r'^$', CollectionView.as_view(), name='collection'),
    url(r'^new/$', CreateView.as_view(), name='new'),
    url(r'^(?P<pk>[^/]+)/$', ArtworkInstanceView.as_view(), name='artwork_instance'),
    url(r'^(?P<pk>[^/]+)/edit/$', EditView.as_view(), name='edit'),
    url(r'^(?P<pk>[^/]+)/delete/$', DeleteView.as_view(), name='delete'),
)
