cottonmouth
===========

Pure-Python HTML generation, inspired by [Hiccup][1].

```python
from cottonmouth.html import render
from cottonmouth.tags import html, head, body, title, meta, link, h1

def welcome(user=None, **context):
    return ['p', 'Welcome' + (' back!' if user else '!')]

content = (
    # Feel free to use raw HTML
    '<!doctype html>',
    # Tags are represented as sequences with a tag name at the head
    [html,
        # Or just use strings instead of the default tag symbols
        ['head',
            [title, 'The Site'],
            # Attributes are passed as a dict immediately after the tag
            [meta, {'charset': 'utf-8'}],
            [link, dict(rel='stylesheet', type='text/css',
                        href='static/layout.css')]],
        [body,
            # You can also call tags as functions with the content as
            # the first argument and attributes as `kwargs`
            [header, h1(u'The Website', id='header')],
            # Use "#id.class" shortcuts to easily create `div` elements
            ['#map.pretty-map'],
            # Functions will be called with context and the results rendered
            ['#main', welcome]]]
)

render(*content, user=None)
```

Equivalent output:

```html
<!doctype html>
<html>
<head>
  <title>The Site</title>
  <meta content="text/html;charset=utf-8" http-equiv="content-type">
  <link href="static/layout.css" type="text/css" rel="stylesheet">
</head>
<body>
  <h1 id="header">Welcome to the site!</h1>
  <div id="map" class="pretty-map"></div>
  <div id="main">
    <p>Welcome!</p>
  </div>
</body>
</html>
```


### Installation

    pip install cottonmouth


### Testing

    python setup.py test


### License

BSD Copyright 2013, Noah Seger


[1]: https://github.com/weavejester/hiccup
