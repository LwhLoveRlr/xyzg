# -*- coding: UTF-8 -*-
import logging
import time
from mongo_config import generate_mongo_conn
import requests
from lxml import etree
import sys

# 设置递归深度限制为新的值（例如10000）
sys.setrecursionlimit(10000000)
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile_path = "./hebei.log"
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
myset = mongodb_laws_2023['xyzg_hebei']
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


def get_data(id, lawtype_code, dict):
    try:
        headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "max-age=0",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://xzzf.hbzwfw.gov.cn/after",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        url1 = "http://xzzf.hbzwfw.gov.cn/punish/getPunishById"
        params1 = {
            "id": id,
            "lawtype": lawtype_code
        }
        response = requests.get(url1, headers=headers1, params=params1, verify=False, proxies=proxy_ip1())
        html = etree.HTML(response.text)
        tables = html.xpath('//table[@class="xzcftable"]')
        for table in tables:
            if len(table.xpath('./tr[1]/td[2]/text()')) >= 1:
                dict['pjtzs'] = table.xpath('./tr[1]/td[2]/text()')[0]
            else:
                dict['pjtzs'] = '无'
            if len(table.xpath('./tr[2]/td[2]/text()')) >= 1:
                dict['xdrmc'] = table.xpath('./tr[2]/td[2]/text()')[0]
            else:
                dict['xdrmc'] = '无'
            if len(table.xpath('./tr[2]/td[4]/text()')) >= 1:
                dict['fddbrxm'] = table.xpath('./tr[2]/td[4]/text()')[0]
            else:
                dict['fddbrxm'] = '无'
            if len(table.xpath('./tr[3]/td[2]/text()')) >= 1:
                dict['tyshxydm'] = table.xpath('./tr[3]/td[2]/text()')[0]
            else:
                dict['tyshxydm'] = '无'
            if len(table.xpath('./tr[4]/td[2]/div/p/text()')) >= 1:
                dict['zywfss'] = table.xpath('./tr[4]/td[2]/div/p/text()')[0]
            else:
                dict['zywfss'] = '无'
            if len(table.xpath('./tr[5]/td[2]/div/text()')) >= 1:
                dict['sy'] = table.xpath('./tr[5]/td[2]/div/text()')[0]
            else:
                dict['sy'] = '无'
            if len(table.xpath('./tr[6]/td[2]/div/text()')) >= 1:
                dict['wfdtk'] = table.xpath('./tr[6]/td[2]/div/text()')[0]
            else:
                dict['wfdtk'] = '无'
            if len(table.xpath('./tr[7]/td[2]/div/text()')) >= 1:
                dict['flyj'] = table.xpath('./tr[7]/td[2]/div/text()')[0]
            else:
                dict['flyj'] = '无'
            if len(table.xpath('./tr[8]/td[2]/text()')) >= 1:
                dict['cfjg'] = table.xpath('./tr[8]/td[2]/text()')[0]
            else:
                dict['cfjg'] = '无'
            if len(table.xpath('./tr[8]/td[4]/text()')) >= 1:
                dict['ssjg'] = table.xpath('./tr[8]/td[4]/text()')[0]
            else:
                dict['ssjg'] = '无'
            if len(table.xpath('./tr[9]/td[2]/text()')) >= 1:
                dict['jdrm'] = table.xpath('./tr[9]/td[2]/text()')[0]
            else:
                dict['jdrm'] = '无'
            if len(table.xpath('./tr[9]/td[4]/text()')) >= 1:
                dict['sdrq'] = table.xpath('./tr[9]/td[4]/text()')[0]
            else:
                dict['sdrq'] = '无'
            if len(table.xpath('./tr[10]/td[2]/div/a/@href')) >= 1:
                dict['content_tp'] = 'http://xzzf.hbzwfw.gov.cn' + table.xpath('./tr[10]/td[2]/div/a/@href')[0]
            else:
                dict['content_tp'] = '无'
        return dict
    except Exception as e:
        logging.info(f'>>>>>>>>>>>>异常：{e}')
        time.sleep(10)
        headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "max-age=0",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://xzzf.hbzwfw.gov.cn/after",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        url1 = "http://xzzf.hbzwfw.gov.cn/punish/getPunishById"
        params1 = {
            "id": id,
            "lawtype": lawtype_code
        }
        response = requests.get(url1, headers=headers1, params=params1, verify=False, proxies=proxy_ip1())
        html = etree.HTML(response.text)
        tables = html.xpath('//table[@class="xzcftable"]')
        for table in tables:
            if len(table.xpath('./tr[1]/td[2]/text()')) >= 1:
                dict['pjtzs'] = table.xpath('./tr[1]/td[2]/text()')[0]
            else:
                dict['pjtzs'] = '无'
            if len(table.xpath('./tr[2]/td[2]/text()')) >= 1:
                dict['xdrmc'] = table.xpath('./tr[2]/td[2]/text()')[0]
            else:
                dict['xdrmc'] = '无'
            if len(table.xpath('./tr[2]/td[4]/text()')) >= 1:
                dict['fddbrxm'] = table.xpath('./tr[2]/td[4]/text()')[0]
            else:
                dict['fddbrxm'] = '无'
            if len(table.xpath('./tr[3]/td[2]/text()')) >= 1:
                dict['tyshxydm'] = table.xpath('./tr[3]/td[2]/text()')[0]
            else:
                dict['tyshxydm'] = '无'
            if len(table.xpath('./tr[4]/td[2]/div/p/text()')) >= 1:
                dict['zywfss'] = table.xpath('./tr[4]/td[2]/div/p/text()')[0]
            else:
                dict['zywfss'] = '无'
            if len(table.xpath('./tr[5]/td[2]/div/text()')) >= 1:
                dict['sy'] = table.xpath('./tr[5]/td[2]/div/text()')[0]
            else:
                dict['sy'] = '无'
            if len(table.xpath('./tr[6]/td[2]/div/text()')) >= 1:
                dict['wfdtk'] = table.xpath('./tr[6]/td[2]/div/text()')[0]
            else:
                dict['wfdtk'] = '无'
            if len(table.xpath('./tr[7]/td[2]/div/text()')) >= 1:
                dict['flyj'] = table.xpath('./tr[7]/td[2]/div/text()')[0]
            else:
                dict['flyj'] = '无'
            if len(table.xpath('./tr[8]/td[2]/text()')) >= 1:
                dict['cfjg'] = table.xpath('./tr[8]/td[2]/text()')[0]
            else:
                dict['cfjg'] = '无'
            if len(table.xpath('./tr[8]/td[4]/text()')) >= 1:
                dict['ssjg'] = table.xpath('./tr[8]/td[4]/text()')[0]
            else:
                dict['ssjg'] = '无'
            if len(table.xpath('./tr[9]/td[2]/text()')) >= 1:
                dict['jdrm'] = table.xpath('./tr[9]/td[2]/text()')[0]
            else:
                dict['jdrm'] = '无'
            if len(table.xpath('./tr[9]/td[4]/text()')) >= 1:
                dict['sdrq'] = table.xpath('./tr[9]/td[4]/text()')[0]
            else:
                dict['sdrq'] = '无'
            if len(table.xpath('./tr[10]/td[2]/div/a/@href')) >= 1:
                dict['content_tp'] = 'http://xzzf.hbzwfw.gov.cn' + table.xpath('./tr[10]/td[2]/div/a/@href')[0]
            else:
                dict['content_tp'] = '无'
        return dict


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://xzzf.hbzwfw.gov.cn",
    "Referer": "http://xzzf.hbzwfw.gov.cn/after",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "X-Requested-With": "XMLHttpRequest"
}
url = "http://xzzf.hbzwfw.gov.cn/punish/getpunish"


def get_url(curpage):
    try:
        data = {
            "curpage": curpage,
            "departId": "",
            "cityId": "",
            "gkType": "120",
            "selType": "0",
            "bmname": "",
            "ztname": "",
            "startdate": "",
            "enddate": ""
        }
        response = requests.post(url, headers=headers, data=data, verify=False, proxies=proxy_ip1())
        for i in response.json()['list']:
            try:
                # time.sleep(1)
                dict1 = get_data(i['id'], i['lawtype_code'], i)
            except Exception as e:
                time.sleep(10)
                dict1 = get_data(i['id'], i['lawtype_code'], i)
            myset.insert_one(dict1)
            logger.info(f'>>>>>>>>第{curpage}页{i["id"]}获取成功')
    except Exception as e:
        logging.info(f'>>>>>>>>>>>>第{curpage}页异常：{e}')
        time.sleep(5)
        data = {
            "curpage": curpage,
            "departId": "",
            "cityId": "",
            "gkType": "120",
            "selType": "0",
            "bmname": "",
            "ztname": "",
            "startdate": "",
            "enddate": ""
        }
        response = requests.post(url, headers=headers, data=data, verify=False, proxies=proxy_ip1())
        for i in response.json()['list']:
            try:
                time.sleep(1)
                dict1 = get_data(i['id'], i['lawtype_code'], i)
            except Exception as e:
                time.sleep(10)
                dict1 = get_data(i['id'], i['lawtype_code'], i)
            myset.insert_one(dict1)
            logger.info(f'>>>>>>>>第{curpage}页{i["id"]}获取成功')


data = {
    "curpage": '1',
    "departId": "",
    "cityId": "",
    "gkType": "120",
    "selType": "0",
    "bmname": "",
    "ztname": "",
    "startdate": "",
    "enddate": ""
}
response = requests.post(url, headers=headers, data=data, verify=False, proxies=proxy_ip1())
for i in response.json()['list']:
    # time.sleep(1)
    dict = get_data(i['id'], i['lawtype_code'], i)
    myset.insert_one(dict)
    logger.info(f'>>>>>>>>第{1}页{i["id"]}获取成功')
for i in range(2, response.json()['page']['last']+1):
    try:
        get_url(i)
    except Exception as e:
        logging.info(f'>>>>>>>>>>>>第{i}页异常：{e}')
