#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-13
# e-mail: jwfy0902@foxmail.com

from sputnik.SpuDBObject import *
from sputnik.SpuDB import *
from sputnik.SpuDateTime import SpuDateTime
from sputnik.SpuDBObject import *

class Comment(SpuDBObject):
    """
    评论模型
    """
    _table_ = "comment"

    def __init__(self, spudb, spucache, debug):
        SpuDBObject.__init__(self, Comment._table_, spudb, spucache, debug=debug)
        self.id = Field(int, 0, 5, auto_inc=True)
        self.name = Field(str, "", 20)
        self.email = Field(str, "", 50)
        self.title = Field(str, "", 30)
        self.contain = Field(str, "", 140)
        self.category = Field(str, "", 10)
        self.ip = Field(str, "", 20)
        self._id = Field(str, "", 15)
        self.status = Field(int, 0, 5)
        self.time = Field(datetime, SpuDateTime.current_time())
