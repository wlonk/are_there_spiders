from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# We like unique emails, let's have more of those.
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^reviews/', include('phobias.urls', namespace='phobias')),
    # Override the default registration view:
    url(r'^accounts/register/$', RegistrationView.as_view(
            form_class=RegistrationFormUniqueEmail,
        ),
        name='registration_register'
    ),
    url(
        r'^accounts/',
        include('registration.backends.default.urls')
    ),
    url(r'^admin/', include(admin.site.urls)),
)
