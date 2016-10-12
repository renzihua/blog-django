# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt
import requests
from time import time
import base64
from random import randint
import hmac
import hashlib
import qcloud_cos

@csrf_exempt
def upload_image(request, dir_name):
    ##################
    #  kindeditor图片上传返回数据格式说明：
    # {"error": 1, "message": "出错信息"}
    # {"error": 0, "url": "图片地址"}
    ##################
    result = {"error": 1, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)
    file_size =  files.size
    if files:
        # result =upload_file_cdn(files, dir_name,file_size)
        result =image_upload(files, dir_name)

    return HttpResponse(json.dumps(result), content_type="application/json")

#目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%d/%d/' %(today.year,today.month)
    if not os.path.exists(settings.MEDIA_ROOT + dir_name):
        os.makedirs(settings.MEDIA_ROOT + dir_name)
    return dir_name

# 图片上传
def image_upload(files, dir_name):
    #允许上传文件类型
    allow_suffix =['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    relative_path_file = upload_generation_dir(dir_name)
    path=os.path.join(settings.MEDIA_ROOT, relative_path_file)
    if not os.path.exists(path): #如果目录不存在创建目录
        os.makedirs(path)
    file_name=str(uuid.uuid1())+"."+file_suffix
    path_file=os.path.join(path, file_name)
    file_url = settings.MEDIA_URL + relative_path_file + file_name
    open(path_file, 'wb').write(files.file.read()) # 保存图片
    return {"error": 0, "url": file_url}

def upload_file_cdn(files,dir_name,file_size):
    Bucket_name = u"news0test"
    APP_ID = 10068872
    secretID = u"AKIDCHF3f5lWXCwaAcJ46lIdoogO0Us4u6sg"
    secretKey = u"0rb9WkeT7cKrDON9kBVdeUDwb5PYVGqD"
    cdn_url = "http://web.file.myqcloud.com/files/v1/"

    file_url = cdn_url + str(APP_ID) + '/' + Bucket_name + '/' + dir_name + '/' + files.name

    # print file_url

    bucket = u"news0test"
    # cos_client = qcloud_cos.CosClient(APP_ID,secretID,secretKey)

    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # request = qcloud_cos.UploadFileRequest(bucket_name=bucket,cos_path=u'/lgy.jpg',local_path=unicode(os.path.join(BASE_DIR,'lgy.png')))
    # upload_file_ret = cos_client.upload_file(request)
    #
    # print repr(upload_file_ret)
    # 生成签名
    cred = qcloud_cos.CredInfo(APP_ID,secretID,secretKey)  # appid, secret_id, secret_key
    auth_obj = qcloud_cos.Auth(cred)
    multi_effect_signature1 = auth_obj.sign_more(bucket=bucket, cos_path=u'/kindeditor/', expired= int(time()) + 600 )
    print multi_effect_signature1

    # requests请求
    headers = {
        "Host":"web.file.myqcloud.com",
        "Content-Type":"multipart/form-data",
        "Authorization":multi_effect_signature1,
        "Content-Length":str(file_size)
    }
    data = {
        "op":"upload",
        "filecontent":files.file.read()
    }
    r = requests.post(url=file_url, headers= headers, data=data)

    print r.content
    return {"error": 0, "url": file_url}

