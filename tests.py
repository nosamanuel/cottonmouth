import unittest

from cottonmouth import constants
from cottonmouth import tags
from cottonmouth.html import render


class TestHTML(unittest.TestCase):
    def test_p_with_content(self):
        self.assertEqual(render(['p', 'paragraph']), '<p>paragraph</p>')

    def test_div_shortcut_with_content(self):
        self.assertEqual(
            render(['#my.test', 'testing']),
            '<div id="my" class="test">testing</div>'
        )

    def test_div_shortcut_with_classname(self):
        self.assertEqual(
            render(['.test', 'testing']),
            '<div class="test">testing</div>'
        )

    def test_image(self):
        self.assertEqual(
            render(['img', {'src': 'image.png'}]),
            '<img src="image.png">'
        )

    def test_embedded_content_with_conditional_list_item(self):
        image = ['img', {'src': 'embedded.jpg'}]
        self.assertEqual(
            render(['#container', {'data-attr': '123'},
                    image, ['hr'],
                    ['ul',
                        ['li', 'A'],
                        ['li', 'B'],
                        ['li', 'C'],
                        ['li', 'D'],
                        ['li', 'Z'] if False else None]]),
            ('<div data-attr="123" id="container">'
             '<img src="embedded.jpg"><hr>'
             '<ul><li>A</li><li>B</li><li>C</li><li>D</li></ul>'
             '</div>')
        )

    def test_generator(self):
        self.assertEqual(
            render(['#container',
                    ['ul', (['li', l] for l in 'ABCDXYZ' if l < 'X')]]),
            ('<div id="container">'
             '<ul><li>A</li><li>B</li><li>C</li><li>D</li></ul>'
             '</div>')
        )

    def test_callable(self):
        say_hello = lambda name: ['p', 'Hello, {}!'.format(name)]
        self.assertEqual(
            render(['#container', say_hello], name='USER'),
            '<div id="container"><p>Hello, USER!</p></div>'
        )

    def test_p_tag(self):
        self.assertEqual(next(tags.p('paragraph 1')), ['p', {}, 'paragraph 1'])
        self.assertEqual(
            render(['#container', tags.p('paragraph 2')]),
            '<div id="container"><p>paragraph 2</p></div>'
        )

    def test_all_tags(self):
        for tag in constants.HTML_TAGS:
            self.assertTrue(hasattr(tags, tag))

    def test_readme_example(self):
        from cottonmouth.tags import html, head, body, title, meta, link, h1

        def welcome(user=None, **context):
            return ['p', 'Welcome' + (' back!' if user else '!')]

        content = (
            '<!doctype html>',
            [html,
                [head,
                    [title, 'The Site'],
                    [meta, {'http-equiv': 'content-type',
                            'content': 'text/html;charset=utf-8'}],
                    [link, dict(rel='stylesheet', type='text/css',
                                href='static/layout.css')]],
                [body,
                    h1('Welcome to the site!', id='header'),
                    ['#map.pretty-map'],
                    ['#main', welcome]]]
        )
        self.assertTrue(isinstance(render(*content), str))

    def test_unicode_coercion(self):
        object_ = object()
        content = ['p', object_]
        self.assertEqual(
            render(content),
            '<p>{}</p>'.format(str(object_))
        )

    def test_class_name_are_set_via_attributes(self):
        content = ['span', {'class': 'foo'}, 'hello']
        self.assertEqual(
            render(content),
            '<span class="foo">hello</span>'
        )

    def test_class_names_are_extended_via_string_attribute(self):
        content = ['span.foo', {'class': 'bar'}, 'hello']
        self.assertEqual(
            render(content),
            '<span class="foo bar">hello</span>'
        )

    def test_class_names_are_extended_via_list_attribute(self):
        content = ['span.foo', {'class': ['bar', 'baz']}, 'hello']
        self.assertEqual(
            render(content),
            '<span class="foo bar baz">hello</span>'
        )

    def test_class_names_are_extended_via_iterable_attribute(self):
        classes = (_ for _ in ['bar', 'baz'])
        content = ['span.foo', {'class': classes}, 'hello']
        self.assertEqual(
            render(content),
            '<span class="foo bar baz">hello</span>'
        )


if __name__ == '__main__':
    unittest.main()
