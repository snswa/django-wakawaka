# from http://open.e-scribe.com/browser/python/django/apps/protowiki/templatetags/wikitags.py
# copyright Paul Bissex, MIT license
import re
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library, Node, Variable
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from wakawaka.models import WikiPage
from wakawaka.urls import WIKI_SLUG

register = Library()

WIKI_WORDS_REGEX = re.compile(r'\b%s\b' % WIKI_SLUG)


def replace_wikiwords(value, group=None,
                      exists_template=r'<a href="{url:>s}">{slug:>s}</a>',
                      missing_template=r'<a class="doesnotexist" href="{url:>s}">{slug:>s}</a>',
                      ):
    def replace_wikiword(m):
        slug = m.group(1)
        try:
            page = WikiPage.objects.get(slug=slug)
            kwargs = {
                'slug': slug,
            }
            if group:
                url = group.content_bridge.reverse('wakawaka_page', group, kwargs=kwargs)
            else:
                url = reverse('wakawaka_page', kwargs=kwargs)
            return exists_template.format(url=url, slug=slug)
        except ObjectDoesNotExist:
            kwargs = {
                'slug': slug,
            }
            if group:
                url = group.content_bridge.reverse('wakawaka_edit', group, kwargs=kwargs)
            else:
                url = reverse('wakawaka_edit', kwargs=kwargs)
            return missing_template.format(url=url, slug=slug)
    return mark_safe(WIKI_WORDS_REGEX.sub(replace_wikiword, value))


@register.filter
def wikify(value, filter_name=None):
    """Makes WikiWords"""
    if filter_name == 'creole':
        return replace_wikiwords(
            value,
            exists_template=r'[[{url:>s}|{slug:>s}]]',
            missing_template=r'[[{url:>s}|{slug:>s}?]]',
            )
    else:
        # Use default templates
        return replace_wikiwords(value)


class WikifyContentNode(Node):
    def __init__(self, content_expr, group_var):
        self.content_expr = content_expr
        self.group_var = Variable(group_var)

    def render(self, context):
        content = self.content_expr.resolve(context)
        group = self.group_var.resolve(context)
        return replace_wikiwords(content, group)

@register.tag
def wikify_content(parser, token):
    bits = token.split_contents()
    try:
        group_var = bits[2]
    except IndexError:
        group_var = None
    return WikifyContentNode(parser.compile_filter(bits[1]), group_var)
