from jinja2 import Markup
from chunks.templatetags.chunks import ChunkNode, GetChunkNode


def chunk(key, cache_time=0, *args, **kwargs):
    content = ChunkNode(key, cache_time).render({})
    return Markup(content)


def get_chunk(key, *args, **kwargs):
    return GetChunkNode(key, None).get_chunk()
