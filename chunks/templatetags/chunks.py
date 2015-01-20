from django import template
from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import get_language_info, get_language


register = template.Library()

Chunk = models.get_model('chunks', 'chunk')
CACHE_PREFIX = "chunk_"
PARAM_CONFIG_ERROR = "%r tag should have either 2 or 3 arguments"
TAGNAME_ERROR = "%r tag's argument should be in quotes"


def _get_i18n_key(key):
    if settings.USE_I18N:
        lang_code = get_language()
        lang_info = get_language_info(lang_code)
        key = '%s_%s' % (key, lang_info['code'])
    return key


def do_chunk(parser, token):
    # split_contents() knows not to split quoted strings.
    tokens = token.split_contents()
    cache_time = None
    tag_name = None
    key = None
    if len(tokens) < 2 or len(tokens) > 3:
        raise template.TemplateSyntaxError, PARAM_CONFIG_ERROR % tokens[0]
    if len(tokens) == 2:
        tag_name, key = tokens
        cache_time = 0
    if len(tokens) == 3:
        tag_name, key, cache_time = tokens
    key = ensure_quoted_string(key, TAGNAME_ERROR % tag_name)
    return ChunkNode(key, cache_time)


class ChunkNode(template.Node):
    def __init__(self, key, cache_time=0):
        self.key = _get_i18n_key(key)
        self.cache_time = cache_time

    def render(self, context):
        try:
            if hasattr(settings, 'CHUNKS_USE_CACHE') and settings.CHUNKS_USE_CACHE:
                cache_key = CACHE_PREFIX + self.key
                c = cache.get(cache_key)
                if c is None:
                    c = Chunk.objects.get(key=self.key)
                    cache.set(cache_key, c, int(self.cache_time))
            else:
                c = Chunk.objects.get(key=self.key)
            content = c.content
        except Chunk.DoesNotExist:
            content = ''
        return content


def do_get_chunk(parser, token):
    tokens = token.split_contents()
    if len(tokens) != 4 or tokens[2] != 'as':
        raise template.TemplateSyntaxError, 'Invalid syntax. Usage: {%% %s "key" as varname %%}' % tokens[0]
    tagname, key, varname = tokens[0], tokens[1], tokens[3]
    key = ensure_quoted_string(key, "Key argument to %r must be in quotes" % tagname)
    return GetChunkNode(key, varname)


class GetChunkNode(template.Node):
    def __init__(self, key, varname):
        self.key = _get_i18n_key(key)
        self.varname = varname

    def get_chunk(self):
        try:
            chunk = Chunk.objects.get(key=self.key)
        except Chunk.DoesNotExist:
            chunk = None
        return chunk

    def render(self, context):
        context[self.varname] = self.get_chunk()
        return ''


def ensure_quoted_string(string, error_message):
    """
    Check to see if the key is properly double/single quoted and
    returns the string without quotes
    """
    if not (string[0] == string[-1] and string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, error_message
    return string[1:-1]


register.tag('chunk', do_chunk)
register.tag('get_chunk', do_get_chunk)
