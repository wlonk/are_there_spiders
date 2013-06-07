from django.core.urlresolvers import reverse


def login_next(request):
    if request.path == reverse('auth_logout'):
        return {'login_next': ''}
    return {'login_next': '?next=%s' % request.path}
