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
from requests import *
import urllib
from bson import ObjectId
from douban_movie_id import *

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_DATABASE = "dm"
MONGO_COLLECTION = "movie"

DOUBAN_BASIC_URL = "https://api.douban.com/v2/movie/subject/%s"
DOUBAN_URL_TOP_250 = "https://api.douban.com/v2/movie/top250?start=%s&count=%s"
DOWNLINK_URL = "http://www.btbook.net/search/"

_Collection = None

def unicode_to_str(u):
    return u.encode("utf-8")

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

def basic_html_to_formatV1(title, flag):
    """
    NOTICE 2015-05-02 更新
    获取下载链接
    """
    url = DOWNLINK_URL + urllib.quote(title)
    if flag == 1:
        url += ".html"
    else:
        url += "/2-1.html"
    headers = {}
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml'=0.9,image/webp,*/*'=0.8''"
    headers["Accept-Encoding"] = "gzip, deflate, sdch"
    headers["Cookie"] = "right_bottom=3; locale=CN; _gat=1; Hm_lvt_753914550ccbe3146e49ce3fab845366=1427863543,1427871102; Hm_lpvt_753914550ccbe3146e49ce3fab845366=1427871105; _ga=GA1.2.1552069543.1427863543"
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"

    try:
        html = requests.get(url, timeout=5.00, headers=headers)
    except Timeout as e:
        logging.error("抓取下载链接 请求超时！")
        return []
    except ConnectionError as e:
        logging.error("抓取下载链接 dns 连接错误")
        return []
    except HTTPError as e:
        logging.error("抓取下载链接 http 请求错误")
        return []
    except Exception as e:
        logging.error("抓取下载链接 未知错误")
        return []
    if not check_requests_status(html.status_code):
        return []
    h = BeautifulSoup(html.content)
    lists = h.find_all("div", class_="search-item")
    return lists


def downlink_to_list(title, flag=1):
    """
    获取下载链接
    """
    lists = basic_html_to_formatV1(title, flag)
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
    res_list = sorted(res_list, key = lambda item :(item["hot"], item["size"]), reverse=True)
    return res_list

def downlink_to_listV2(title, flag=1):
    """
    NOTICE 2015-05-02
    获取下载链接，格式如同
    [{},{},{size='', url='', name=''}]
    """
    lists = basic_html_to_formatV1(title, flag)
    res_list = []
    for list in lists:

        b = list.find_all("b")
        size = unicode_to_str(b[1].string)
        
        hot = int(unicode_to_str(b[2].string))
        if hot < 10:
            continue
        

        down_link = list.find_all("a", class_="download")
        for link in down_link:
            down_link_dict = {}
            down_link_dict["size"] = size
            down_link_dict["url"] = link.get("href")
            down_link_dict["name"] = link.string

            res_list.append(down_link_dict)
    res_list = sorted(res_list, key = lambda item :(item["size"], item["url"]), reverse=True)
    return res_list


def douban_top_250(start=0, count=100):
    """
    获取豆瓣电影的前面250部评分最高的电影id
    存入到一个文件中去
    """
    contains = requests.get(DOUBAN_URL_TOP_250 %(start, count))
    if not check_requests_status(contains.status_code):
        return None
    text = contains.text
    text = json.loads(text)
    items = text.get("subjects")

    ids = []
    for item in items:
        print("douban ID %s" %(item["id"]))
        ids.append(item["id"]+"\n")

    files = open("../log/topid.log", "a")
    files.writelines(ids)
    files.close()

def read_top_250():
    douban_top_250()
    douban_top_250(100)
    douban_top_250(200)

def douban_to_dict(id):
    """
    通过豆瓣的电影id，读取json，然后返回字典
    NOTICE:筛选掉电影描述字段太短了的电影数据
    """
    contains = requests.get(DOUBAN_BASIC_URL %(id))
    if not check_requests_status(contains.status_code):
        return {}, 0
    
    text = contains.text
    text = json.loads(text)
    movie = {}
    movie["rating"] = text.get("rating")
    movie["year"] = text.get("year")
    movie["origin_image"] = text.get("images")
    movie["image"] = {}
    
    movie["summary"] = text.get("summary")
    if len(movie["summary"]) < 20:
        return {}, 0
    
    for k, v in text.get("images", "{}").iteritems():
        image_url = v
        url = store_url(image_url, "douban-"+k)
        time.sleep(1.0)
        if url:
            movie["image"][k] = url
    movie["id"] = unicode_to_str(text.get("id"))
    movie["title"] = text.get("title")
    movie["category"] = text.get("genres")
    movie["countries"] = text.get("countries")
    movie["casts"] = []
    for cast in text.get("casts"):
        movie["casts"].append(cast["name"])
    
    movie["original_title"] = text.get("original_title")
    movie["subtype"] = text.get("subtype")
    movie["directors"] = []
    for director in text.get("directors"):
        movie["directors"].append(director["name"])
    movie["aka"] = text.get("aka")
    
    #movie["down_link"] = downlink_to_list(unicode_to_str(movie["title"]))
    movie["down_link"] = downlink_to_listV2(unicode_to_str(movie["title"]))
    movie["status"] = "online"
    movie_link_flag = 1
    if not movie["down_link"]:
        movie_link_flag = 0
        print("%s 未获取下载链接" %(movie["id"]))
    return movie, movie_link_flag

def check_mongo_id(_id):
    """
    监测mongo是否存在数据
    """
    if not _Collection:
        mongo_init()
    try:
        flag = _Collection.find_one({"_id":ObjectId(_id)})
    except Exception as e:
        flag = False
    if flag:
        return True
    return False

def update_down_format(id=""):
    """
    NOTICE time: 2015-05-01  修改存储格式 
    由于之前存储的数据格式过于复杂，现在修改为
    [{},{},{size='', url='', name=''}]
    """
    if not _Collection:
        mongo_init()
    try:
        if not id:
            rets = _Collection.find()
        else:
            rets = _Collection.find({"_id":ObjectId(id)})
        num = 0
        for ret in rets:
            _id = ret["_id"]
            down = ret.get("down_link","")
            if not down:
                # 这是没有下载链接的
                continue
            flag = down[0].get("hot", "")
            if not flag:
                # 说明了已经是处理的了
                continue
            num += 1
            down_list = []
            for do in down:
                size = do["size"]
                for k, v in do["link"].iteritems():
                    d_dict = {}
                    d_dict["size"] = size
                    d_dict["name"] = k
                    d_dict["url"] = v
                    down_list.append(d_dict)
            _Collection.update({"_id":_id},{"$set":{"down_link":down_list}})
            print "["+str(num)+"]"+"成功转换下载格式   "+str(_id)
    except Exception as e:
        print(e)

def write_to_mongo(id):
    """
    dict store to mongo
    """
    if not _Collection:
        mongo_init()
    flag = _Collection.find_one({"id":id})
    if flag:
        # 说明已经有数据了，无需添加
        return 0, "已经存在相关数据，添加失败"
    movie_dict, flag = douban_to_dict(id)
    if not movie_dict:
        return -1, "暂无有效数据"
    _id = _Collection.insert(movie_dict)
    return str(_id), flag

def get_topids():
    files = open("../log/topid.log")
    ids = files.readlines()
    files.close()
    return ids

def get_ids(tag="爱情", id=1):
    """
    NOTICE ADD in 2015-05-06 21:10
    主要是为了添加更多的电影数据
    """
    doubanid = DouBanId(tag, id)
    doubanid.get_url()
    ids = doubanid.query()
    return ids

def main():
    #id = '1764796'
    ids = get_ids()
    files = open("../log/record-%s.log" %(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time()))), "wb+")
    for id in ids:
        id = int(id)
        _id, flag = write_to_mongo(id)
        if not _id:
            files.write("豆瓣ID %d 以添加\n"  %(id))
            continue
        if _id == -1:
            files.write("豆瓣ID %d 无数据\n"  %(id))
            continue
        print "%s\n" %(_id)
        if flag:
            files.write("豆瓣ID %d 存储_id %s\n"  %(id, _id))
        else:
            files.write("豆瓣ID %d 存储_id %s 没有获取下载链接\n"  %(id, _id))

    files.close()
    
if __name__ == "__main__":
    import ipdb
    ipdb.set_trace()
    #id = "552758a9e206a514e2257ac5"
    #check_mongo_id(id)
    #read_top_250()
    main()
    #douban_to_dict(1764796)
    #title = "超能陆战队"
    #downlink_to_list(title)
    update_down_format()
