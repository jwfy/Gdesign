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

ACCESS_KEY = "GNdXddPogJmjge7P_26hHONuulBirv0fcUVX8IhY"
SECRET_KEY = "VRfWmKm8VNuwimm51iRaSEpDyFptIDn0D2caxfAr"
BUCKET_NAME = "movie"
BASIC_URL = "http://7xib6a.com1.z0.glb.clouddn.com/%s"

def store_file_to_qiniu(image):
    auth = Auth(access_key=ACCESS_KEY, secret_key=SECRET_KEY)
    put_policy = {
            "fsizeLimit":10000,
            "returnBody": "name=$(fname)&size=$(fsize)"
    }
    key = image["file_name"] + "-" + str(int(time.time()))
    mime_type = image["content-type"]
    data = image["body"]
    token = auth.upload_token(bucket=BUCKET_NAME, key=key)
    ret, info = put_data(token, key, data, mime_type=mime_type, check_crc=True)
    if info.status_code == 200:
        return BASIC_URL %(key)
    return None
