from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from .forms import ReviewForm
from .mixins import LoginRequiredMixin
from .models import Review


class CollectionView(ListView):
    model = Review
    template_name = 'phobias/review_list.html'


class CreateView(FormView, LoginRequiredMixin):
    form_class = ReviewForm
    template_name = 'phobias/review_form.html'

    def form_valid(self, form):
        review = form.save(self.request.user)
        return redirect(review)


class InstanceView(DetailView):
    model = Review
    template_name = 'phobias/review_instance.html'


class EditView(FormView, LoginRequiredMixin):
    pass


class DeleteView(FormView, LoginRequiredMixin):
    pass
