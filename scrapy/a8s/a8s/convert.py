#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import codecs

ARTICLES_DIR = os.path.join(os.path.abspath(os.path.join(__file__,
                            '../../../../')), '_posts', 'articles')

TEMPLATE = u"""---
layout: post
title: {title}
excerpt: from {source}
categories: articles
tags: [{source}]
link: {link}
author: {source}
share: true
---

"""


def extract_name(slug):
    return sorted(slug.split('.'), key=len)[-1]


def get_content(item):
    res = ''
    if 'ingredients' in item:
        res += '### Ingredients\n\n'
        for ingredient in item['ingredients']:
            res += '<span><input type="checkbox"> %s</span><br>\n' % ingredient
        res += '\n\n### Recipe\n\n'
    res += 'Go check the recipe instructions on [%s](%s).' % \
        (item['source'], item['link'])
    return res


if __name__ == "__main__":
    json_items_file = sys.argv[1]
    with open(json_items_file, 'r') as src:
        for item in json.load(src):
            source_dir = os.path.join(ARTICLES_DIR,
                                      extract_name(item['source']))
            if not os.path.exists(source_dir):
                os.makedirs(source_dir)
            with codecs.open(os.path.join(source_dir,
                             item['slug'] + '.md'),
                             'w+', 'utf-8') as article:
                body = article.read().split('---\n')[-1].strip('\n')
                article.seek(0)
                article.write(TEMPLATE.format(title=item['title'].title(),
                              source=item['source'],
                              link=item['link'],
                              ))
                if body:
                    article.write(body)
                else:
                    article.write(get_content(item))
