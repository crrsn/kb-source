# -*- encoding: utf-8 -*-
# kb v0.1.6
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kb printer for count chinese word module

:Copyright: © 2022, gnc.
:License: GPLv3 (see /LICENSE).
"""

import re

# for count_zh_word function used to count the chinese word
zh_pattern = re.compile(u'[\u4e00-\u9fff]+')


def count_zh_word(word):
    '''
        count the chinese word number
    Args:
        word: input string

    Returns:
        num_zh: number of chinese word
    '''

    num_zh = 0
    # if word like 'menu_好吃鬆餅_仁愛店.png', the re.findall will return [4, 3] array
    for _zh_word in re.findall(zh_pattern, word):
        num_zh += len(_zh_word)

    return num_zh