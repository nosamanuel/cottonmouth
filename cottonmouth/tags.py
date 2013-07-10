from . import constants


class Tag(unicode):
    def __call__(self, *content, **extra):
        tag = [unicode(self), extra]
        tag.extend(content)
        yield tag


exports = locals()
for tag in constants.HTML_TAGS:
    exports[tag] = Tag(tag)
