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
---
"""

if __name__ == "__main__":
    json_items_file = sys.argv[1]
    with open(json_items_file, 'r') as src:
        for item in json.load(src):
            with codecs.open(os.path.join(ARTICLES_DIR, item['slug'] + '.md'),
                             'w', 'utf-8') as article:
                article.write(TEMPLATE.format(title=item['title'],
                              source=item['source'],
                              link=item['link'],
                              ))
