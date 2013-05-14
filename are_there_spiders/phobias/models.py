from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class Artwork(models.Model):
    ARTWORK_CHOICES = (
        ('book', 'Book'),
        ('movie', 'Movie'),
        ('videogame', 'Video Game'),
    )

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=10, choices=ARTWORK_CHOICES)
    creator = models.CharField(max_length=100)
    year = models.IntegerField(default=2010)

    def __unicode__(self):
        return "%s's %s (%s)" % (
            self.creator,
            self.name,
            self.get_kind_display(),
        )


class TaggedReview(TaggedItemBase):
    content_object = models.ForeignKey('Review')


class Review(models.Model):
    SPIDER_QUANTITY_CHOICES = (
        ('none', 'None'),
        ('sortof', 'Sort of'),
        ('rarely', 'Rarely'),
        ('often', 'Often'),
        ('beware', 'Beware'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    artwork = models.ForeignKey(Artwork)
    spider_quantity = models.CharField(
        max_length=10,
        choices=SPIDER_QUANTITY_CHOICES
    )
    spider_quality = TaggableManager(
        through=TaggedReview,
        blank=True,
        verbose_name=u'Spider quality'
    )
    summary = models.TextField(max_length=1000)

    def __unicode__(self):
        return "Review of %s by %s" % (
            self.artwork,
            self.user.username
        )

    def get_absolute_url(self):
        return reverse('phobias:instance', kwargs={'pk': self.pk})
