from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class Artwork(models.Model):
    ARTWORK_CHOICES = (
        ('book', 'Book'),
        ('movie', 'Movie'),
        ('videogame', 'Video Game'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
    kind = models.CharField(max_length=10, choices=ARTWORK_CHOICES)
    creator = models.CharField(max_length=100)
    year = models.IntegerField(default=2010)

    def __unicode__(self):
        return "%s's %s (%s)" % (
            self.creator,
            self.name,
            self.get_kind_display(),
        )

    def get_absolute_url(self):
        return reverse('phobias:artwork_instance', kwargs={'slug': self.slug})

    def active_reviews(self):
        return self.review_set.filter(marked_as_spam=False)


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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    spider_quantity = models.CharField(
        max_length=10,
        choices=SPIDER_QUANTITY_CHOICES
    )
    spider_quality = TaggableManager(
        through=TaggedReview,
        blank=True,
        verbose_name=u'Spider quality'
    )
    summary = models.TextField(max_length=1000, blank=True)
    flagged_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='flagged_reviews'
    )
    marked_as_spam = models.BooleanField(default=False)

    @property
    def flagged_count(self):
        return self.flagged_by.count()

    def __unicode__(self):
        return "%s by %s" % (
            self.artwork,
            self.user.username
        )

    def get_absolute_url(self):
        return reverse('phobias:edit', kwargs={'pk': self.pk})
