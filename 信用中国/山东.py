# -*- coding: UTF-8 -*-
import logging
import sys
import time
from mongo_config import generate_mongo_conn

import execjs
import requests
# 设置递归深度限制为新的值（例如10000）
sys.setrecursionlimit(10000000)
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile_path = "./jx.log"
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
myset = mongodb_laws_2023['xyzg_sdon']

def get_content(tyshxydm, kw, page):
    try:
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Origin": "https://credit.shandong.gov.cn",
            "Pragma": "no-cache",
            "Referer": "https://credit.shandong.gov.cn/creditsearch.creditdetailindexbgca.dhtml?entityType=1&kw"
                       "=91371524673171488G&tyshxydm=91371524673171488G",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "^\\^Not.A/Brand^^;v=^\\^8^^, ^\\^Chromium^^;v=^\\^114^^, ^\\^Google",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^"
        }
        url = "https://credit.shandong.gov.cn/creditsearch.creditdetalicayth.phtml"
        timestamp = int(time.time() * 1000)
        token = execjs.compile(open('sd.js', encoding='utf-8').read()).call('get_token', kw, timestamp)
        params = {
            'page': page,
            'type': '行政管理',
            'Category': 'credit_xyzx_fr_xzcf_new',
            "kw": kw,
            "call": "2",
            "token": token,
            "timestamp": timestamp,
        }
        response = requests.post(url, headers=headers, params=params)
        for i in response.json()['catalogSearch']['list']:
            i['tyshxydm'] = tyshxydm  # 社会信用代码
            i['jgmc'] = kw  # 机关名称
            myset.insert_one(i)
            logging.info(i)
            logger.info(f'>>>>>>>>保存成功{i["cf_wsh"]}')
        if page == 1:
            max_num = int(response.json()['catalogSearch']['total'])
            num = int(max_num / 10)
            if num % 10 != 0:
                num += 1
            for j in range(2, num + 1):
                page += 1
                get_content(tyshxydm, kw, num)
    except Exception as e:
        logging.info(f'>>>>>>>异常{e}')


def get_kw(kw):
    try:
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Origin": "https://credit.shandong.gov.cn",
            "Pragma": "no-cache",
            "Referer": "https://credit.shandong.gov.cn/creditsearch.creditdetailindexbgca.dhtml?entityType=1&kw"
                       "=91371524673171488G&tyshxydm=91371524673171488G",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "^\\^Not.A/Brand^^;v=^\\^8^^, ^\\^Chromium^^;v=^\\^114^^, ^\\^Google",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^"
        }
        url = "https://credit.shandong.gov.cn/creditsearch.creditdetalicayth.phtml"
        timestamp = int(time.time() * 1000)
        token = execjs.compile(open('sd.js', encoding='utf-8').read()).call('get_token', kw, timestamp)
        params = {
            "call": "1",
            "kw": kw,
            "token": token,
            "timestamp": timestamp,
            "tyshxydm": kw
        }
        response = requests.post(url, headers=headers, params=params)
        kw1 = response.json()['baseinfo']['headEntity']['jgmc']
        page = 1
        get_content(kw, kw1, page)
    except Exception as e:
        logging.info(f'异常{e}')


def get_my(page):
    try:
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Origin": "https://credit.shandong.gov.cn",
            "Referer": "https://credit.shandong.gov.cn/creditsearch.punishmentList.phtml?id=&CreditKey=",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "^\\^Not_A",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^"
        }
        url1 = "https://credit.shandong.gov.cn/creditsearch.hqpass.phtml"
        params1 = {
            "kw": ""
        }
        response1 = requests.post(url1, headers=headers, params=params1)
        url = "https://credit.shandong.gov.cn/creditsearch.creditsgsindexcayth.phtml"
        params = {
            "type": "行政处罚",
            "kw": "",
            "page": page,
            "my": response1.json()['success']
        }
        response = requests.post(url, headers=headers, params=params)
        for i in response.json()['typeNameAndCountSearch']['list']:
            print(i['tyshxydm'])
            get_kw(i['tyshxydm'])
    except Exception as e:
        logging.info(e)


for i in range(1, 51):
    get_my(i)
