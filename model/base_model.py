#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-26
# e-mail: jwfy0902@foxmail.com

from config import mongo
from bson import ObjectId
from sputnik.SpuLogging import SpuLogging

"""
仿照sputnik的orm结构写的类似与mongodb的orm模块
"""

class BaseMongoModel(object):
    
    __fields__ = {}
    __collection__ = ""
    _id = ""

    _logging = SpuLogging(module_name='base_model', class_name='BaseMongoModel')

    def __init__(self):
        pass

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def fields(self):
        return self.__fields__.keys()

    @classmethod
    def dict_to_model(cls, _dict):
        if not isinstance(_dict, dict):
            cls._logging.error("dict_to_model [%s] error!" % str(_dict))
            return None
        if "_id" in _dict:
            _id = str(_dict["_id"])
            _dict["id"] = _id
        model = cls()
        for field in model.fields:
            v = _dict.get(field, None)
            if v is None:
                v = model.__fields__[field][1]
            if isinstance(v, unicode):
                v = v.encode("utf8")
            v = model.__fields__[field][0](v)
            setattr(model, field, v)
        return model

    @classmethod
    def model_to_list(cls, model_list):
        lists = []
        for model in model_list:
            lists.append(model.to_dict())
        return lists

    def to_dict(self):
        model_json = {}
        for field in self.__fields__:
            v = getattr(self, field, None)
            if v is None:
                v = self.__fields__[field][1]
            v = self.__fields__[field][0](v)
            model[fiel] = v
        return model_json

    def update(self):
        #TODO
        pass

    def insert(self):
        _dict = self.to_dict()
        
