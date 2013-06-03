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
    url(r'^reviews/new/$', CreateView.as_view(), name='new'),
    url(r'^artworks/(?P<slug>[^/]+)/$', ArtworkInstanceView.as_view(), name='artwork_instance'),
    url(r'^reviews/(?P<pk>[^/]+)/edit/$', EditView.as_view(), name='edit'),
    url(r'^reviews/(?P<pk>[^/]+)/delete/$', DeleteView.as_view(), name='delete'),
)
