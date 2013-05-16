from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, DeleteView

from taggit.utils import edit_string_for_tags

from .forms import ReviewForm
from .mixins import LoginRequiredMixin, OwnerRequiredMixin
from .models import Review


class CollectionView(ListView):
    model = Review
    template_name = 'phobias/review_list.html'


class CreateView(LoginRequiredMixin, FormView):
    form_class = ReviewForm
    template_name = 'phobias/review_form.html'

    def form_valid(self, form):
        review = form.save(self.request.user)
        return redirect(review)


class InstanceView(DetailView):
    model = Review
    template_name = 'phobias/review_instance.html'


class EditView(SingleObjectMixin, OwnerRequiredMixin, FormView):
    model = Review
    form_class = ReviewForm
    template_name = 'phobias/review_form.html'

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super(EditView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        """
        We want to populate the form with data from the two associated models,
        and so we have to use initial, not instance, as this is not a
        ModelForm.

        So we basically slurp and serialize two models.
        """
        review = self.get_object()
        # Dumbest possible serialization that could work
        # @todo: this isn't very DRY.
        artwork = review.artwork
        initial = dict(
            artwork_name=artwork.name,
            artwork_kind=artwork.kind,
            artwork_creator=artwork.creator,
            artwork_year=artwork.year,
            spider_quantity=review.spider_quantity,
            spider_quality=edit_string_for_tags(review.spider_quality.all()),
            summary=review.summary
        )
        return initial

    def form_valid(self, form):
        review = form.save(self.request.user)
        return redirect(review)


class DeleteView(OwnerRequiredMixin, DeleteView):
    model = Review
    template_name = 'phobias/review_confirm_delete.html'
    # Seems ugly that we have to namespace this in the app.
    success_url = reverse_lazy('phobias:collection')
