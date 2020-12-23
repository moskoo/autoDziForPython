#!/usr/bin/env python3

# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import time
import os.path
import uuid

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = ''      # 替换为用户的 secretId
secret_key = ''      # 替换为用户的 secretKey
region = ''     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
bucket = '' #桶名称
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)

#### 高级上传接口（推荐）
# 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
def upload_big(filePath):
    dir = time.strftime("%Y-%m-%d")
    filename = uuid.uuid4().hex + os.path.splitext(filePath)[1]
    prfile = 'tool_upload/' + str(dir) + "/" + filename
    response = client.upload_file(
        Bucket=bucket,
        LocalFilePath=filePath,
        Key=prfile,
        PartSize=1,
        MAXThread=10,
        EnableMD5=False
    )
    if('url' in response):
        # 修改了cos_client.py
        return response['url']
    else:
        # 自己组装url
        return scheme + '://' + bucket + '.cos.' + region + '.myqcloud.com/' + prfile

def upload_dzi(dzi_path):
    dir = time.strftime("%Y-%m-%d")

    filepath, tmpfilename = os.path.split(dzi_path)
    shotname, extension = os.path.splitext(tmpfilename)
    prfile = 'tool_upload/dzi/' + str(dir) + "/" + tmpfilename
    response = client.upload_file(
        Bucket=bucket,
        LocalFilePath=dzi_path,
        Key=prfile,
        PartSize=1,
        MAXThread=10,
        EnableMD5=False
    )
    qie_dir = filepath + "/" + shotname + "_files"
    all_files = all_files_path(qie_dir)
    if all_files:
        for i in all_files:
            local_path = i.replace(qie_dir, 'tool_upload/dzi/' + str(dir) + '/' + shotname + "_files")
            client.upload_file(
                Bucket=bucket,
                LocalFilePath=i,
                Key=local_path,
                PartSize=1,
                MAXThread=10,
                EnableMD5=False
            )
    if('url' in response):
        # 修改了cos_client.py
        return response['url']
    else:
        # 自己组装url
        return scheme + '://' + bucket + '.cos.' + region + '.myqcloud.com/' + prfile

def all_files_path(rootDir):
    filepaths = []
    for root, dirs, files in os.walk(rootDir):  # 分别代表根目录、文件夹、文件
        for file in files:  # 遍历文件
            file_path = os.path.join(root, file)  # 获取文件绝对路径
            extension = os.path.splitext(file_path)[1]
            if(extension in ['.jpg','.png','.gif','jpeg']):
                filepaths.append(file_path)  # 将文件路径添加进列表
        for dir in dirs:  # 遍历目录下的子目录
            dir_path = os.path.join(root, dir)  # 获取子目录路径
            all_files_path(dir_path)  # 递归调用
    return filepaths

