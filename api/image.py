#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-04-23
# e-mail: jwfy0902@foxmail.com

from base import *
from module.image_ctrl import ImageCtrl

image_ctrl = ImageCtrl()

class image(WebRequest):
    _logging = SpuLogging(module_name="image", class_name="image")

    def __init__(self):
        pass
    
    def captcha(self):
        """
        获取验证码
        """
        pass

    @POST_FILE('image')
    def file(self, image):
        """
        上传文件
        """
        import ipdb
        ipdb.set_trace()
        url = image_ctrl.file_upload(image)
        return self._write(111)

    @POST
    def url(self, url={"atype":"unicode", "adef":""}):
        """
        根据图片上传，可识别中文
        """
        # TODO
        pass

