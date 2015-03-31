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
import ipdb
sys.path.insert(0, "../module/")
from base_ctrl import *

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DATABASE = "dm"
MONGO_COLLECTION = "movie"

DOUBAN_BASIC_URL = "https://api.douban.com/v2/movie/subject/%s"
DOWNLINK_URL = "http://www.btbook.net/search/"

_Collection = None

def mongo_init():
    """
    mongo 数据库 初始化
    """
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    database = client[MONGO_DATABASE]
    collection = database[MONGO_COLLECTION]
    global _Collection
    _Collection = collection

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

def downlink_to_list(title, flag=1):
    """
    bs4 正则解析html，获取下载链接
    """
    url = DOWNLINK_URL + urllib.quote(title)
    if flag == 1:
        url += ".html"
    else:
        url += "/2-1.html"
    html = requests.get(url)
    if not check_requests_status(html.status_code):
        return {}
    h = BeautifulSoup(html.content)
    lists = h.find_all("div", class_="search-item")
    res_list = []
    for list in lists:
        rst_dict = {}
        
        b = list.find_all("b")
        rst_dict["size"] = unicode_to_str(b[1].string)
        rst_dict["hot"] = int(unicode_to_str(b[2].string))
        
        if rst_dict["hot"] < 10:
            continue

        down_link_dict = {}
        down_link = list.find_all("a", class_="download")
        for link in down_link:
            down_link_dict[link.string] = link.get("href")

        rst_dict["link"] = down_link_dict
        res_list.append(rst_dict)
    return res_list
    
def douban_to_mongo(id):
    """
    通过豆瓣的电影id，读取json，然后返回字典
    """
    contains = requests.get(DOUBAN_BASIC_URL %(id))
    if not check_requests_status(contains.status_code):
        return {}
    text = contains.text
    text = json.loads(text)
    movie = {}
    movie["rating"] = text.get("rating")
    movie["year"] = text.get("year")
    movie["origin_image"] = text.get("images")
    movie["image"] = {}
    for k, v in text.get("images", "{}").iteritems():
        image_url = v
        url = store_url(image_url, "douban-"+k)
        time.sleep(1.0)
        if url:
            movie["image"][k] = url
    movie["id"] = text.get("id")
    movie["title"] = text.get("title")
    movie["category"] = text.get("genres")
    movie["countries"] = text.get("countries")
    movie["casts"] = []
    for cast in text.get("casts"):
        movie["casts"].append(cast["name"])
    
    movie["original_title"] = text.get("original_title")
    movie["summary"] = text.get("summary")
    movie["subtype"] = text.get("subtype")
    movie["directors"] = []
    for director in text.get("directors"):
        movie["directors"].append(director["name"])
    movie["aka"] = text.get("aka")
    
    movie["down_link"] = downlink_to_list(unicode_to_str(movie["title"]))

    _id = write_to_mongo(movie)
    return _id

def write_to_mongo(movie_dict):
    """
    dict store to mongo
    """
    if not _Collection:
        mongo_init()
    id = _Collection.insert(movie_dict).str
    return id

def main():
    id = '1764796'
    files = open('./douban.txt', 'wb')
    _id = douban_to_mongo(id)
    print "%s\n" %(_id)
    files.write("存入数据库id=%s\n" %(_id))
    files.close()
    

if __name__ == "__main__":
    main()
    #douban_to_dict(1764796)
    #title = "超能陆战队"
    #downlink_to_list(title)
