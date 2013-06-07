from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from .views import (
    CollectionView,
    CreateView,
    FlagReviewView,
    ArtworkInstanceView,
    EditView,
    DeleteView,
    SearchView
)

urlpatterns = patterns(
    '',  # No prefix
    url(
        r'^$',
        RedirectView.as_view(url=reverse_lazy(
            'collection',
            kwargs={
                'kind': 'book'
            }
        )),
        name='collection_base'
    ),
    url(r'^reviews/new/$', CreateView.as_view(), name='new'),
    url(
        r'^artworks/(?P<slug>[^/]+)/$',
        ArtworkInstanceView.as_view(),
        name='artwork_instance'
    ),
    url(r'^reviews/(?P<pk>[^/]+)/edit/$', EditView.as_view(), name='edit'),
    url(
        r'^reviews/(?P<pk>[^/]+)/delete/$',
        DeleteView.as_view(),
        name='delete'
    ),
    url(
        r'^reviews/(?P<pk>[^/]+)/flag/$',
        FlagReviewView.as_view(),
        name='flag'
    ),
    url(r'search/$', SearchView.as_view(), name='search'),
    # Fallthrough to this:
    url(r'(?P<kind>[^/]+)/$', CollectionView.as_view(), name='collection'),
)
