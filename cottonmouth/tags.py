from . import constants


class Tag(str):
    def __call__(self, *content, **extra):
        tag = [str(self), extra]
        tag.extend(content)
        yield tag


exports = locals()
for tag in constants.HTML_TAGS:
    exports[tag] = Tag(tag)
