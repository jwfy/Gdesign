#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author:jwfy
# time: 2015-04-10
# e-amil: jwfy0902@foxmail.com

from sputnik.SpuDBObject import *
from sputnik.SpuDB import *
from sputnik.SpuDateTime import SpuDateTime
from sputnik.SpuDBObject import *

class User(SpuDBObject):
    """
    用户模型
    """
    _table_ = "user"

    def __init__(self, spudb, spucache, debug):
        SpuDBObject.__init__(self, User._table_, spudb, spucache, debug=debug)
        self.id = Field(int, 0, 5, auto_inc=True)
        self.name = Field(str, "", 20)
        self.email = Field(str, "", 50)
        self.password = Field(str, "", 200)
        self.login_time = Field(datetime, SpuDateTime.current_time())
        self.register_time = Field(datetime, "")
        self.permission = Field(int, 0, 5)
        self.status = Field(int, 0, 5)
