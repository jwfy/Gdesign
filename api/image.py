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
        获取验证码，写入session
        NOTICE: data = "movie"
                url = "http://7xib6a.com1.z0.glb.clouddn.com/captcha-2015-04-30-16:53:35" 
        """
        try:
            data,url = image_ctrl.captcha_image()
            if data:
                self._set_captcha_session(data)
            else:
                self._set_captcha_session()
                url = "http://7xib6a.com1.z0.glb.clouddn.com/captcha-2015-04-30-16:53:35"
        except Exception as e:
            self._logging.error(e)
            self._set_captcha_session()
            url = "http://7xib6a.com1.z0.glb.clouddn.com/captcha-2015-04-30-16:53:35"
        return self._write(dict({"url":url}))

    @POST_FILE('file')
    def file(self, file):
        """
        上传文件
        """
        if not file:
            return self._write(dict({"url":""}))
        image = file[0]
        store_img = {}
        store_img["name"] = image["filename"]
        store_img["mime_type"] = image["content_type"]
        store_img["body"] = image["body"]
        url = image_ctrl.file_upload(store_img, "file-upload")
        ans = {}
        ans["url"] = url
        return self._write(ans)

    @POST
    def url(self, url={"atype":"unicode", "adef":""}):
        """
        根据图片上传，可识别中文
        """
        # TODO
        pass

