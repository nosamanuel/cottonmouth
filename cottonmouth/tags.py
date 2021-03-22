import six
from . import constants


class Tag(six.text_type):
    def __call__(self, *content, **extra):
        tag = [six.text_type(self), extra]
        tag.extend(content)
        yield tag


exports = locals()
for tag in constants.HTML_TAGS:
    exports[tag] = Tag(tag)
