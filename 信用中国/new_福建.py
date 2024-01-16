import logging
import time

import requests
from lxml import etree

from mongo_config import generate_mongo_conn
from 图片解码 import decode_image
from Chaojiying_Python.chaojiying_Python.chaojiying import Chaojiying_Client
import sys

# 设置递归深度限制为新的值（例如10000）
sys.setrecursionlimit(10000000)
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile_path = "./fj.log"
fh = logging.FileHandler(logfile_path, mode='a')
fh.setLevel(logging.DEBUG)  # 用于写到file的等级开关
# 第三步，再创建一个handler,用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

# 第四步，定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)
logging.getLogger("elasticsearch").setLevel(logging.WARNING)

mongodb_laws_2023 = generate_mongo_conn()
myset = mongodb_laws_2023['xyzg_fjian']

def proxy_ip1():
    PROXY_META = "http://%(user)s:%(pass)s@%(server)s" % {
        "server": "tunnel2.qg.net:13794",
        "user": "B8B99831",
        "pass": "E1BE0439B5D9",
    }
    PROXIES = {
        "http": PROXY_META,
        "https": PROXY_META,
    }
    return PROXIES

def get_content(dataId):
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Referer": "https://xy.fujian.gov.cn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "randomId": "",
            "sec-ch-ua": "^\\^Not_A",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^"
        }
        url = "https://xy.fujian.gov.cn/credit/cmpinternetportalfront/doublepublicity/detail"
        params = {
            "dataId": dataId,
            "type": "行政处罚",
            "resourceId": ""
        }
        response = requests.get(url, headers=headers, params=params, proxies=proxy_ip1())
        data = response.json()['data']['columnShowList']['records'][0]
        myset.insert_one(data)
        logger.info(f'>>>>>>>>>{data["id"]}保存成功')
    except Exception as e:
        logging.info(f'>>>>>>>>>>异常{e}')

def get_data(pageNo):
    try:
        headers = {
            "Host": "xy.fujian.gov.cn",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
            "Accept": "application/json, text/plain, */*",
            "randomId": "",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://xy.fujian.gov.cn/",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        }
        url = "https://xy.fujian.gov.cn/credit/cmpinternetportalfront/doublepublicity/getPunishList"
        params = {
            "pageSize": "15",
            "pageNo": pageNo,
            "keyword": ""
        }
        response = requests.get(url, headers=headers, params=params, proxies=proxy_ip1())
        time.sleep(1)
        dict = response.json()['data']
        if 'columnShowList' in dict:
            if 'records' in dict['columnShowList']:
                if response.json()['data']['columnShowList']['records']:
                    for records in response.json()['data']['columnShowList']['records']:
                        get_content(records['id'])
    except Exception as e:
        logging.info(f'>>>>>>>>>>验证码验证{e}')
        headers = {
            "Host": "xy.fujian.gov.cn",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
            "Accept": "application/json, text/plain, */*",
            "randomId": "",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://xy.fujian.gov.cn/",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        }
        url = "https://xy.fujian.gov.cn/credit/cmpinternetportalfront/doublepublicity/getPermitList"
        params = {
            "pageSize": "15",
            "pageNo": pageNo,
            "keyword": ""
        }
        response = requests.get(url, headers=headers, params=params, proxies=proxy_ip1())
        html = etree.HTML(response.text)
        verifyId = html.xpath('//input[@id="verifyId"]/@value')[0]
        url = "https://xy.fujian.gov.cn/credit/kk-anti-reptile/refresh"
        params = {
            "verifyId": verifyId
        }
        response1 = requests.post(url, headers=headers, params=params, proxies=proxy_ip1())
        decode_image(response1.json()['verifyImgStr'])
        chaojiying = Chaojiying_Client('15269797859', '36CSNp.BApJ6Ebj', '942408')
        im = open('验证码.jpg', 'rb').read()
        img_data = chaojiying.PostPic(im, 1005)
        pic_str = img_data['pic_str']
        url = "https://xy.fujian.gov.cn/credit/kk-anti-reptile/validate"
        params = {
            "verifyId": response1.json()['verifyId'],
            "realRequestUri": "/credit/cmpinternetportalfront/doublepublicity/getPermitList",
            "result": pic_str
        }
        response = requests.post(url, headers=headers, params=params, proxies=proxy_ip1())
        headers = {
            "Host": "xy.fujian.gov.cn",
            "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
            "Accept": "application/json, text/plain, */*",
            "randomId": "",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://xy.fujian.gov.cn/",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
        }
        url = "https://xy.fujian.gov.cn/credit/cmpinternetportalfront/doublepublicity/getPunishList"
        params = {
            "pageSize": "15",
            "pageNo": pageNo,
            "keyword": ""
        }
        response1 = requests.get(url, headers=headers, params=params, proxies=proxy_ip1())
        time.sleep(5)
        logging.info('验证成功')
        dict = response.json()['data']
        if 'columnShowList' in dict:
            if 'records' in dict['columnShowList']:
                if response.json()['data']['columnShowList']['records']:
                    for records in response.json()['data']['columnShowList']['records']:
                        get_content(records['id'])
for pageNo in range(1, 101):
    try:
        get_data(pageNo)
    except Exception as e:
        pass
