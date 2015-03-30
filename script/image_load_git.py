#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-28
# e-mail: jwfy0902@foxmail.com


import logging
from qiniu import Auth
from qiniu import put_file, put_data
from qiniu import BucketManager
from base64 import urlsafe_b64encode as safeb64
import time
import requests
from io import BytesIO
from captcha.image import ImageCaptcha
import random
import string

ACCESS_KEY = "*****"
SECRET_KEY = "****"
BUCKET_NAME = "*****"
BASIC_URL = "*****%s"

_auth = None

def init():
    auth = Auth(access_key=ACCESS_KEY, secret_key=SECRET_KEY)
    global _auth
    _auth = auth

def upload_image(url):
    """
    url = "******.jpg"
    """
    image_type = ['image/jpeg', 'image/pjpeg', 'image/gif', 'image/png', 'image/x-icon'] 
    if not url:
        logging.error("url 错误")
        return None
    try:
        image_content = requests.get(url)
        image = {}
        if image_content.headers["content-type"] in image_type:
            image["mime_type"] = image_content.headers["content-type"]
            image["body"] = image_content.content
            image["name"] = url.split("/")[-1].split(".")[0]
            return image
    except Exception as e:
        logging.error("图片解析错误")
        return None

def store_bindata(image):
    """
    image = {"name", "mime_type", "body"}
    """
    if not _auth:
        init()
    key = image["name"] + "-" + str(int(time.time()))
    mime_type = image["mime_type"]
    data = image["body"]
    token = _auth.upload_token(bucket=BUCKET_NAME, key=key)
    ret, info = put_data(token, key, data, mime_type=mime_type, check_crc=True)
    if info.status_code == 200:
        return BASIC_URL %(key)
    return None

def store_url(url):
    """
    根据 url 存储 图片
    """
    pass


def store_file(url):
    """
    根据 文件 存储 图片
    """
    pass

def captcha(height=50, width=120):
    """
    随机生成验证码，然后存为图片，生成对应的地址
    返回其url 和 对应的 captcha_name
    """
    try:
        image = ImageCaptcha(height=height, width=width, fonts=['ComicSansMS.ttf'], font_sizes=[40])
        captcha_name = "".join(random.sample(string.letters + string.digits, 4))
        data = image.generate(captcha_name)
        image = {}
        image["name"] = "captcha"
        image["mime_type"] = "image/png"
        image["body"] = data.getvalue()
        url = store_bindata(image)
        return captcha_name, url
    except Exception as e:
        logging.error(e)
        return None

if __name__ == "__main__":
    name, url = captcha()
    print name
    print url
