#! /usr/bin/env python
# -*- coding: utf-8 -*-

# author: jwfy
# time: 2015-03-28
# e-mail: jwfy0902@foxmail.com


import logging
from qiniu import Auth
from qiniu import put_file
from qiniu import BucketManager
from base64 import urlsafe_b64encode as safeb64

ACCESS_KEY = "GNdXddPogJmjge7P_26hHONuulBirv0fcUVX8IhY"
SECRET_KEY = "VRfWmKm8VNuwimm51iRaSEpDyFptIDn0D2caxfAr"
BUCKET_NAME = "movie"

def qiniu_init():
    pass


def store_file_to_qiniu(file):
    auth = Auth(access_key=ACCESS_KEY, secret_key=SECRET_KEY)
    put_policy = {
            "fsizeLimit":10000,
            "returnBody": "name=$(fname)&size=$(fsize)"
    }
    key = image["file_name"] 
    type = image["content-type"]
    import ipdb
    ipdb.set_trace()
    token = auth.upload_token(bucket=BUCKET_NAME, key=key, policy=put_policy)
    ret, info = put_file(up_token=token, key=key, file_path=image_url, mime_type=type, check_crc=True)
    print ret
    print info

def store_url_to_qiniu(url):
    """
    """
    pass

def url_to_name(url):

