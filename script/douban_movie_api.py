#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author:jwfy
# time: 2015-03-27
# e-mail:jwfy0902@foxmail.com

"""
这是一个脚本库，主要的操作是读取豆瓣电影的数据，然后解析成对应的字典数据，同时
如果其中有图片，则获取对应的图片，存到qiniu  中，
针对具体的名称，解析包含种子下载链接的html，获取正确的下载连接
最后最后 存到mongo 中
"""

from  pymongo import MongoClient
import time
import datetime
import json
import sys
import os
import logging
from image_load import *
from bs4 import BeautifulSoup
import requests
import urllib


MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DATABASE = "dm"
MONGO_COLLECTION = "movie"

DOUBAN_BASIC_URL = "https://api.douban.com/v2/movie/subject/%s"
DOWNLINK_URL = "http://www.btbook.net/search/"


def mongo_init():
    """
    mongo 数据库 初始化
    """
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    database = client[MONGO_DATABASE]
    collection = database[MONGO_COLLECTION]
    return collection

def check_requests_status(status):
    """
    检查requests返回的数据，状态码
    """
    if status == 200:
        return True
    elif status == 201:
        return True
    elif status == 202:
        return True
    elif status == 400:
        logging.error("请求地址不存在或者参数错误")
        return False
    elif status == 401:
        logging.error("未授权访问")
        return False
    elif status == 403:
        logging.error("被禁止访问")
        return False
    elif status == 404:
        logging.error("请求的资源不存在")
        return False
    elif status == 500:
        logging.error("服务器内部错误")
        return False
    else:
        logging.error("未知错误")
        return False

def downlink_to_dict(title, flag=1):
    """
    bs4 正则解析html，获取下载链接
    """
    import ipdb
    ipdb.set_trace()
    url = DOWNLINK_URL + urllib.quote(title)
    if flag == 1:
        url += ".html"
    else:
        url += "/2-1.html"
    html = requests.get(url)
    h = BeautifulSoup(html.content)
    lists = h.find_all("div", class_="search-item")
    for list in lists:
        pass

    


def douban_to_dict(id):
    """
    通过豆瓣的电影id，读取json，然后返回字典
    """
    contains = requests.get(DOUBAN_BASIC_URL %(id))
    if not check_requests_status(contains.status_code):
        return {}
    text = contains.text
    text = json.loads(text)
    movie = {}
    movie["rating"] = text["rating"]
    movie["year"] = text["year"]
    movie["origin_image"] = text["images"] 
    movie["image"] = {}
    for image in text["images"]:
        image_url = text["images"][image]
        url = store_url(image_url)
        if url:
            movie["image"][image] = url
    movie["id"] = text["id"]
    movie["title"] = text["title"]
    movie["category"] = text["genres"]
    movie["countries"] = text["countries"]
    movie["casts"] = []
    for cast in text["casts"]:
        movie["casts"].append(cast["name"])
    
    movie["original_title"] = text["original_title"]
    movie["summary"] = text["summary"]
    movie["subtype"] = text["subtype"]
    movie["directors"] = []
    for director in text["directors"]:
        movie["directors"].append(director["name"])
    movie["aka"] = text["aka"]
    time.sleep(1.5)
    import ipdb
    ipdb.set_trace()
    print movie

    
if __name__ == "__main__":
    #douban_to_dict(1764796)
    title = "超能陆战队"
    downlink_to_dict(title)
