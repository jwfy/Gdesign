#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-31
# e-mail: jwfy0902@foxmail.com

import time
import hashlib
import inspect

def unicode_to_str(u):
    """
    unicode to str
    """
    return u.encode("utf-8")

def unicode_to_md5(u):
    """
    unicode to str to md5
    """
    u = unicode_to_str(u)
    return hashlib.md5(u).hexdigest()


