from django import forms

from taggit.utils import parse_tags

from .models import Artwork, Review


class ReviewForm(forms.Form):
    review_id = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )
    artwork_name = forms.CharField()
    artwork_kind = forms.ChoiceField(choices=Artwork.ARTWORK_CHOICES)
    artwork_creator = forms.CharField(required=False)
    artwork_year = forms.IntegerField(required=False)
    artwork_season = forms.CharField(required=False)
    artwork_episode = forms.CharField(required=False)

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
            year=self.cleaned_data['artwork_year'],
        )
        if artwork.kind == 'show':
            # Allow unlimited reviews:
            review, created = Review.objects.get_or_create(
                pk=self.cleaned_data['review_id'],
                user=user,
                artwork=artwork,
                season=self.cleaned_data['artwork_season'],
                episode=self.cleaned_data['artwork_episode'],
            )
        else:
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
