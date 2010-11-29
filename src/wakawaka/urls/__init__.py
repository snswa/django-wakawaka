from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from wakawaka import views
from wakawaka.settings import WIKI_SLUG


def decorated_urlpatterns(decorator):
    """Return an urlpatterns for wakawaka, with all views decorated."""
    return patterns('',
        url(r'^$', decorator(views.index), name='wakawaka_index'),

        # Revision and Page list
        url(r'^history/$', decorator(views.revision_list), name='wakawaka_revision_list'),
        url(r'^index/$', decorator(views.page_list), name='wakawaka_page_list'),

        # Revision list for page
        url(r'^(?P<slug>%s)/history/$' % WIKI_SLUG, decorator(views.revisions), name='wakawaka_revision_list'),

        # Changes between two revisions, revision id's come from GET
        url(r'^(?P<slug>%s)/changes/$' % WIKI_SLUG, decorator(views.changes), name='wakawaka_changes'),

        # Edit Form
        url(r'^(?P<slug>%s)/edit/(?P<rev_id>\d+)/$' % WIKI_SLUG, decorator(login_required(views.edit)), name='wakawaka_edit'),
        url(r'^(?P<slug>%s)/edit/$' % WIKI_SLUG, decorator(login_required(views.edit)), name='wakawaka_edit'),

        # Page
        url(r'^(?P<slug>%s)/rev(?P<rev_id>\d+)/$' % WIKI_SLUG, decorator(views.page), name='wakawaka_page'),
        url(r'^(?P<slug>%s)/$' % WIKI_SLUG, decorator(views.page), name='wakawaka_page'),
    )


urlpatterns = decorated_urlpatterns(lambda v: v)
