#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-05-05
# e-mail: jwfy0902@foxmail.com

"""
[docs]:https://pythonhosted.org/pyquery/
[docs]http://www.douban.com/tag/%E7%88%B1%E6%83%85/movie?start=30
[docs]http://www.douban.com/tag/%E5%BC%A0%E8%89%BA%E8%B0%8B/movie?start=15
"""

from pyquery import PyQuery as pq
import requests
import urllib
import urlparse

class DouBanId(object):

    def __init__(self, tag="爱情", id=1):
        """
        主要是解析豆瓣电影的相关id,抓取
        """
        self.tag = tag
        self.id = id
        self.url = ""
    
    def set_tag(self, tag):
        self.tag = tag

    def set_id(self, id):
        self.id = id

    def get_url(self):
        tag = self.tag
        id = self.id
        self.url = "http://www.douban.com/tag/%s/movie?start=%s" %(urllib.quote(tag), id)

    def query(self):
        d = pq(url=self.url)
        ds = d(".movie-list").find("dd > a")
        ids = []
        for d in ds:
            uri = d.values()[0]
            # 解析参数
            res = urlparse.urlparse(uri)
            params = urlparse.parse_qs(res.query, True)
            id = params["object_id"][0]
            title = d.text
            print id, title
            ids.append(id)
        return ids

if __name__ == "__main__":
    douban = DouBanId()
    import ipdb
    ipdb.set_trace()
    douban.get_url()
    ids = douban.query()
