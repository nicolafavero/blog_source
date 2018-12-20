#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Leonardo Giordani'
SITENAME = u'The Digital Cat'
SITESUBTITLE = "Adventures of a curious cat in the land of programming"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'atom.xml'
TAG_FEED_ATOM = 'categories/%s/atom.xml'
CATEGORY_FEED_ATOM = 'category/%s/atom.xml'
TRANSLATION_FEED_ATOM = None
DISPLAY_FEEDS_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = False

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.do']}

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = CATEGORY_URL + 'index.html'

TAG_URL = 'categories/{slug}/'
TAG_SAVE_AS = TAG_URL + 'index.html'

ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = ARCHIVES_URL + 'index.html'

AUTHOR_URL = 'authors/{slug}/'
AUTHOR_SAVE_AS = AUTHOR_URL + 'index.html'

PLUGIN_PATHS = ["../pelican-plugins"]
PLUGINS = ['related_posts', 'series', 'sitemap', 'tag_cloud']

GOOGLE_ANALYTICS_UNIVERSAL = 'UA-74364524-1'

SITEMAP = {
    'format': 'xml',
}

SLUG_SUBSTITUTIONS = [("c++","cpp")]

DEFAULT_DATE_FORMAT = '%d/%m/%Y'

SOCIAL = (
        ('Twitter', 'https://twitter.com/thedigicat'),
        ('Google+', 'https://plus.google.com/u/0/111444750762335924049'),
        ('GitHub', 'https://github.com/TheDigitalCatOnline'),
    )

DEFAULT_PAGINATION = 9
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
    )

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'code', 'notebooks', 'files', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
TWITTER_USERNAME = 'thedigicat'

THEME = "../editorial"

FAVICON = 'images/TheDigitalCat_favicon_32.png'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {
            'permalink': True
        },
    },
    'output_format': 'html5',
}