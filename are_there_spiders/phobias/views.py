from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, DeleteView

from taggit.utils import edit_string_for_tags

from .forms import ReviewForm
from .mixins import LoginRequiredMixin, OwnerRequiredMixin
from .models import Review, Artwork


class CollectionView(ListView):
    model = Artwork
    template_name = 'phobias/artwork_list.html'


class CreateView(LoginRequiredMixin, FormView):
    form_class = ReviewForm
    template_name = 'phobias/review_form.html'

    def get_initial(self):
        """
        If someone gets here from an artwork page, let's give them a head-
        start.
        """
        if 'artwork' not in self.request.GET:
            return super(CreateView, self).get_initial()

        initial = {}
        try:
            artwork = Artwork.objects.get(pk=self.request.GET.get('artwork'))
        except (Artwork.DoesNotExist, Artwork.MultipleObjectReturned):
            pass
        else:
            initial['artwork_name'] = artwork.name
            initial['artwork_kind'] = artwork.kind
            initial['artwork_creator'] = artwork.creator
            initial['artwork_year'] = artwork.year
        return initial

    def form_valid(self, form):
        review = form.save(self.request.user)
        return redirect(review.artwork)


class ArtworkInstanceView(DetailView):
    model = Artwork
    template_name = 'phobias/artwork_instance.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArtworkInstanceView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated():
            if context['artwork'].review_set.filter(user=user).count() > 0:
                context['review_on_page'] = True
            else:
                context['review_on_page'] = False
        return context


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
        return redirect(review.artwork)


class DeleteView(OwnerRequiredMixin, DeleteView):
    model = Review
    template_name = 'phobias/review_confirm_delete.html'
    # Seems ugly that we have to namespace this in the app.
    success_url = reverse_lazy('phobias:collection')
