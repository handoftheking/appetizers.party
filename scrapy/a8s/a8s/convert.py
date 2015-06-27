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
title: %s
excerpt: from %s
categories: articles
tags: [%s]
link: %s
---
"""


if __name__ == "__main__":
    print(ARTICLES_DIR)
    with open(sys.argv[1], 'r') as src:
        for item in json.load(src):
            with codecs.open(os.path.join(ARTICLES_DIR, item['slug'] + '.md'),
                             'w', 'utf-8') as article:
                article.write(TEMPLATE % (
                              item['title'],
                              item['source'],
                              item['source'],
                              item['link']))
