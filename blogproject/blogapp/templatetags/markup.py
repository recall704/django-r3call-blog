from django import template
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def gfm_markdown(value):
    from markdown import markdown as md
    html = md(value,extensions=['gfm'])
    return mark_safe(html)