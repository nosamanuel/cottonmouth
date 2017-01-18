import collections
import itertools

from . import constants


def render(*content, **context):
    """
    Renders a sequence of content as HTML.
    """
    return u''.join((e for c in content for e in render_content(c, **context)))


def render_content(content, **context):
    """
    Renders Python data as HTML.

    Content can be one of the following:

      - A string containing raw HTML, rendered as-is
      - A callable that will be called with the current **context
      - A sequence beginning with a literal HTML tag name
      - Any other value, coerced to unicode
    """
    if content is None:
        yield u''
    elif isinstance(content, basestring):
        yield content
    elif callable(content):
        for e in render_content(content(**context), **context):
            yield e
    elif isinstance(content, collections.Iterable):
        for e in render_iterable(content, **context):
            yield e
    else:
        yield unicode(content)


def render_iterable(content, **context):
    """
    Renders a list, tuple, or generator of content as HTML.
    """
    tail = iter(content)
    head = next(tail)

    # Render tag around the content
    if isinstance(head, basestring):
        for e in render_tag(head, tail, **context):
            yield e
    # Render nested lists
    elif isinstance(head, collections.Iterable):
        for e in render_iterable(head, **context):
            yield e
        for content in tail:
            for e in render_content(content, **context):
                yield e


def render_tag(tag, content, **context):
    """
    Renders an HTML tag with its content.
    """
    try:
        # Parse extra attributes and remainder
        content, remainder = itertools.tee(content)
        extra = dict(**next(remainder))
    except StopIteration:
        # If there is no remainder, we just render the tag
        extra, remainder = {}, []
    except TypeError:
        # There are no extra attributes
        extra, remainder = {}, content

    # Default to div if no explicit tag is provided
    if tag.startswith(u'#'):
        tag = u'div{}'.format(tag)
    elif tag.startswith(u'.'):
        tag = u'div{}'.format(tag)

    # Split tag into ["tag#id", "class1", "class2", ...] chunks
    chunks = tag.split('.')

    # Parse tag and id out of tag shortcut
    tag = chunks[0]
    if u'#' in chunks[0]:
        tag, extra['id'] = chunks[0].split('#')

    # Parse classes
    classes = chunks[1:]
    extra_classes = extra.get('class')
    if isinstance(extra_classes, basestring):
        classes.extend(extra_classes.split())
    elif extra_classes:
        classes.extend(extra_classes)

    # Format classes
    if classes:
        extra['class'] = u' '.join(classes)

    # Format attributes
    attributes = u''.join([u' {}="{}"'.format(*i) for i in extra.items()])

    # Start our tag sandwich
    yield u'<{}{}>'.format(tag, attributes)

    # Render the delicious filling or toppings
    for content in remainder:
        for e in render_content(content, **context):
            yield e

    # CLOSE THE TAG IF WE HAVE TO I GUESS
    if tag not in constants.HTML_VOID_TAGS:
        yield u'</{}>'.format(tag)
