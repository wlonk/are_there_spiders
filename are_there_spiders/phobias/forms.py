from django import forms

from taggit.utils import parse_tags

from .models import Artwork, Review


class ReviewForm(forms.Form):
    artwork_name = forms.CharField()
    artwork_kind = forms.ChoiceField(choices=Artwork.ARTWORK_CHOICES)
    artwork_creator = forms.CharField()
    artwork_year = forms.IntegerField()

    spider_quantity = forms.ChoiceField(
        choices=Review.SPIDER_QUANTITY_CHOICES
    )
    spider_quality = forms.CharField(
        required=False,
        help_text='Comma-separated list of spider descriptors.'
    )
    summary = forms.CharField(widget=forms.Textarea, required=False)

    def clean_artwork_name(self):
        data = self.cleaned_data['artwork_name']
        return data.title()

    def clean_artwork_creator(self):
        data = self.cleaned_data['artwork_creator']
        return data.title()

    def save(self, user):
        artwork, created = Artwork.objects.get_or_create(
            name=self.cleaned_data['artwork_name'],
            kind=self.cleaned_data['artwork_kind'],
            creator=self.cleaned_data['artwork_creator'],
            year=self.cleaned_data['artwork_year']
        )
        review, created = Review.objects.get_or_create(
            user=user,
            artwork=artwork,
        )
        review.spider_quantity = self.cleaned_data['spider_quantity']
        review.summary = self.cleaned_data['summary']
        review.spider_quality.set(
            *parse_tags(self.cleaned_data['spider_quality'])
        )
        review.save()
        return review
