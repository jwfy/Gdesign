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


import requests
from  pymongo import MongoClient
import time
import datetime
import json
import sys
import os
from sae.storage import Bucket, Connection
import logging
from qiniu_image_upload import *


MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DATABASE = "dm"
MONGO_COLLECTION = "movie"

DOUBAN_BASIC_URL = "https://api.douban.com/v2/movie/subject/%s"

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

def get_image_content(url):
    """
    获取图片url具体的内容，然后存储到qiniu 中
    """
    image_type = ['image/jpeg', 'image/pjpeg', 'image/gif', 'image/png', 'image/x-icon']
    if url:
        try:
            img_content = requests.get(url)
            image = {}
            if img_content.headers["content-type"] in image_type:
                image["content-type"] = img_content.headers["content-type"]
                file_type = image["content-type"].split("/")[-1]
                image["file_name"] = url.split("/")[-1].split(".")[0]
                image["body"] = img_content.content
            return image
        except Exception as e:
            logging.error("图片解析错误")
            return None

def sae_init():
    conn = Connection(accesskey=SAE_ACCESS_KEY, secretkey=SAE_SECRET_KEY, account=SAE_APP_NAME)
    bucket = Bucket("b", conn)
    return bucket

def image_upload(image):
    """
    上面获取到的图片，然后上传到sae storage中,得到其中的url
    """
    url = store_file_to_qiniu(image)
    print url

def douban_to_dict(id):
    """
    通过豆瓣的电影id，读取json，然后返回字典
    """
    contains = requests.get(DOUBAN_BASIC_URL %(id))
    time.sleep(1.5)
    if not check_requests_status(contains.status_code):
        return []
    text = contains.text
    text = json.loads(text)
    movies = {}
    
    
if __name__ == "__main__":
    #douban_to_dict(1764796)
    url = "http://img3.douban.com/view/movie_poster_cover/ipst/public/p494284924.jpg"
    url = "http://img3.douban.com/view/movie_poster_cover/lpst/public/p494284924.jpg"
    s = get_image_content(url)
    image_upload(s)
