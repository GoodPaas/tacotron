#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 xiaominfc(武汉鸣鸾信息科技有限公司) <xiaominfc@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import os

wordsDict = {}
_align_f = open(os.path.split(os.path.realpath(__file__))[0] + '/zh_lang/align_lexicon.txt','r')
_line = _align_f.readline()
while _line:
    _line = _line.strip();
    _parts = _line.split('\t')
    if len(_parts) == 2 and _parts[0] not in wordsDict:
        wordsDict[_parts[0]] = _parts[1]
    _line = _align_f.readline()


def sentence_to_pinyin(sentence):
    parts = sentence.split(' ')
    text = ""
    for i in range(0, len(parts)):
        word = parts[i]
        if word in wordsDict:
            if len(text) > 0:
                text = text + ' '
            text = text + wordsDict[word]       
    return text

