#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-23
# e-mail: jwfy0902@foxmail.com

from script.image_load import *
from sputnik.SpuLogging import SpuLogging
from base_ctrl import *

class ImageCtrl(object):
    _logging = SpuLogging()

    def __init__(self):
        pass

    def url_image(self, url):
        """
        根据图片文件进行上传，存储，返回url值
        """
        try:
            name = 'url-load'
            url = store_url(url=url, name=name, source=0)
            return url
        except Exception as e:
            self._logging.error(e)
            return None

    def file_image(self, file):
        """
        根据url进行上传，存储，返回url值
        """
        # TODO 还未完成
        store_file(file)
        pass
    
    def captcha_image(self, height=50, width=100):
        """
        生成验证码，然后返回url
        """
        try:
            data, url = captcha(height, width)
            return data, url
        except Exception as e:
            return None
