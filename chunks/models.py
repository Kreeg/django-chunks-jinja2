# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache
from django.conf import settings


class Chunk(models.Model):
    """
    A Chunk is a piece of content associated
    with a unique key that can be inserted into
    any template with the use of a special template
    tag
    """
    key = models.CharField(_(u'Key'), help_text=_(u"A unique name for this chunk of content"),
                           blank=False, max_length=255, unique=True)
    content = models.TextField(_(u'Content'), blank=True)
    description = models.CharField(_(u'Description'), blank=True, max_length=64, help_text=_(u"Short Description"))

    class Meta:
        verbose_name = _(u'chunk')
        verbose_name_plural = _(u'chunks')

    def __unicode__(self):
        return u"%s" % (self.key,)


def chunk_cache_post(sender, instance, *args, **kwargs):
    if settings.USE_I18N:
        keys = ['chunk_%s_%s' % (instance.key, lang) for lang, name in settings.LANGUAGES]
    else:
        keys = ['chunk_%s' % instance.key]
    cache.delete_many(keys)

post_save.connect(chunk_cache_post, sender=Chunk)
post_delete.connect(chunk_cache_post, sender=Chunk)