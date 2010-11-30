from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class WikiPage(models.Model):
    slug = models.CharField(_('slug'), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    group = generic.GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("Wiki page")
        verbose_name_plural = _("Wiki pages")
        ordering = ['slug']
        permissions = (
            ("can_view", "Can view the wiki."),
            ("reset_lock", "Can reset the edit lock of a wiki page."),
        )

    def __unicode__(self):
        return self.slug

    @property
    def current(self):
        return self.revisions.latest()

    @property
    def rev(self, rev_id):
        return self.revisions.get(pk=rev_id)

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }
        group = self.group
        if group:
            return group.content_bridge.reverse('wakawaka_page', group, kwargs)
        else:
            return reverse('wakawaka_page', kwargs=kwargs)


class Revision(models.Model):
    page = models.ForeignKey(WikiPage, related_name='revisions')
    content = models.TextField(_('content'))
    message = models.TextField(_('change message'), blank=True)
    creator = models.ForeignKey(User, blank=True, null=True, related_name='wakawaka_revisions')
    creator_ip = models.IPAddressField(_('creator ip'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True, db_index=True)

    class Meta:
        verbose_name = _("Revision")
        verbose_name_plural = _("Revisions")
        ordering = ['-modified']
        get_latest_by = 'modified'

    def get_absolute_url(self):
        kwargs = {
            'slug': self.page.slug,
            'rev_id': self.pk,
        }
        group = self.page.group
        if group:
            return group.content_bridge.reverse('wakawaka_page', group, kwargs)
        else:
            return reverse('wakawaka_page', kwargs=kwargs)

    def __unicode__(self):
        return ugettext('Revision %(created)s for %(page_slug)s') % {
            'created': self.created.strftime('%Y%m%d-%H%M'),
            'page_slug': self.page.slug,
        }

