#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-13
# e-mail: jwfy0902@foxmail.com

from sputnik.SpuDBObject import *
from sputnik.SpuDB import *
from sputnik.SpuDateTime import SpuDateTime
from sputnik.SpuDBObject import *

class MovieReComment(SpuDBObject):
    """
    首页电影推荐模型
    """
    _table_ = "movie_recomment"

    def __init__(self, spudb, spucache, debug):
        SpuDBObject.__init__(self, MovieReComment._table_, spudb, spucache, debug=debug)
        self.id = Field(int, 0, 5, auto_inc=True)
        self._id = Field(str, "", 30)
        self.status = Field(int, 0, 5)
        self.title = Field(str, "", 20)
        self.img_url = Field(str, 0, 200)
        self.time = Field(datetime, SpuDateTime.current_time())
        self.update_time = Field(datetime, SpuDateTime.current_time())
