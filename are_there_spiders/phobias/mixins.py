from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class OwnerRequiredMixin(object):
    """
    This mixin must be used with SingleObjectMixin from
    django.views.generic.detail.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user != self.get_object().user:
            # Forbidden, but we return a not-found. This is following GitHub's
            # approach, where people shouldn't even know about what they're
            # not allowed to do. Because this is human-facing, and not a
            # RESTful API, I don't feel dirty doing this.
            raise Http404
        return super(OwnerRequiredMixin, self).dispatch(*args, **kwargs)
