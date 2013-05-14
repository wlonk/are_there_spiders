from django.views.generic import ListView, DetailView

from .models import Review


class CollectionView(ListView):
    model = Review
    template_name = 'phobias/review_list.html'


class InstanceView(DetailView):
    model = Review
    template_name = 'phobias/review_instance.html'
