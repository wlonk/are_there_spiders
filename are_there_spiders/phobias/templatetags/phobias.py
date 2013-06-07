import re
from urllib import urlencode

from django import template
from django.template.base import TemplateSyntaxError

kwarg_re = re.compile(r"(\w+)=(.+)")

register = template.Library()


class QueryStringNode(template.Node):
    def __init__(self, qs, replacements):
        self.qs = qs
        self.replacements = replacements

    def render(self, context):
        qs_copy = template.Variable(self.qs).resolve(context).copy()
        for k, v in self.replacements.items():
            self.replacements[k] = template.Variable(v).resolve(context)
        qs_copy.update(self.replacements)
        if self.qs:
            try:
                return '?' + urlencode(qs_copy)
            except:
                return ''
        else:
            return ''


@register.tag
def qs(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "'%s' takes at least one argument (dict or multidict)" % bits[0])
    dict_or_multidict = bits[1]
    replacements = bits[2:]
    kwargs = {}
    for replacement in replacements:
        match = kwarg_re.match(replacement)
        if not match:
            raise TemplateSyntaxError("Malformed arguments to qs tag")
        name, value = match.groups()
        kwargs[name] = value
    return QueryStringNode(dict_or_multidict, kwargs)


@register.filter
def autofocus(field):
    field.field.widget.attrs['autofocus'] = '1'
    return field
