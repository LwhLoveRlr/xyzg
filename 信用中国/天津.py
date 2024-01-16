# -*- coding: UTF-8 -*-
import logging
import time
from mongo_config import generate_mongo_conn
import requests
from lxml import etree
import re
import sys

# 设置递归深度限制为新的值（例如10000）
sys.setrecursionlimit(10000000)
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile_path = "./tj.log"
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
myset = mongodb_laws_2023['xyzg_tjing']


def get_data(recid, recflag, messageid, dict):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Referer": "https://credit.fzgg.tj.gov.cn/xygs/datalist.do",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "sec-ch-ua": "^\\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^"
    }
    url = "https://credit.fzgg.tj.gov.cn/xygs/showDetail.do"
    params = {
        "recid": recid,
        "messageid": messageid,
        "recflag": recflag,
        "d": int(time.time() * 1000)
    }
    response = requests.get(url, headers=headers, params=params)
    html = etree.HTML(response.text)
    dict['cf_type'] = html.xpath('//table[@class="table table-bordered"]/tr[3]/td[2]/text()')[0].strip()
    dict['cfyj'] = html.xpath('//table[@class="table table-bordered"]/tr[4]/td[2]/text()')[0].strip()
    dict['xzcfjdws'] = html.xpath('//table[@class="table table-bordered"]/tr[5]/td[2]/text()')[0].strip()
    dict['sjlydw_tyshxydm'] = html.xpath('//table[@class="table table-bordered"]/tr[6]/td[2]/text()')[
        0].strip()
    dict['sjlydw'] = html.xpath('//table[@class="table table-bordered"]/tr[7]/td[2]/text()')[0].strip()
    dict['cfjg_tyshxydm'] = html.xpath('//table[@class="table table-bordered"]/tr[8]/td[2]/text()')[
        0].strip()
    dict['wfss'] = html.xpath('//table[@class="table table-bordered"]/tr[9]/td[2]/text()')[0].strip()
    dict['wfxw_type'] = html.xpath('//table[@class="table table-bordered"]/tr[10]/td[2]/text()')[0].strip()
    dict['cfjg'] = html.xpath('//table[@class="table table-bordered"]/tr[11]/td[2]/text()')[0].strip()
    dict['fkje'] = html.xpath('//table[@class="table table-bordered"]/tr[12]/td[2]/text()')[0].strip()
    dict['cfjdrq'] = html.xpath('//table[@class="table table-bordered"]/tr[13]/td[2]/text()')[0].strip()
    dict['gsjzq'] = html.xpath('//table[@class="table table-bordered"]/tr[14]/td[2]/text()')[0].strip()
    dict['content'] = html.xpath('//table[@class="table table-bordered"]/tr[15]/td[2]/text()')[0].strip()
    return dict


def get_html(pageNo):
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://credit.fzgg.tj.gov.cn",
            "Referer": "https://credit.fzgg.tj.gov.cn/xygs/datalist.do",
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "sec-ch-ua": "^\\^Not_A",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\\^Windows^^"
        }

        url = "https://credit.fzgg.tj.gov.cn/xygs/datalist.do"
        data = {
            "pageNo": f"{pageNo}",
            "pageSize": "10",
            "messageid": "51BAD61AAD244B499E470ABD8E0EB9DF",
            "domainid": "017",
            "condition": "",
            "paramMap['CF_XDR_MC']": "",
            "paramMap['CF_XDR_SHXYM']": "",
            "paramMap['CF_WSH']": "",
            "paramMap['CF_JDRQ_start']": "",
            "paramMap['CF_JDRQ_end']": "",
            "yzm": ""
        }
        response = requests.post(url, headers=headers, data=data)
        obj = re.compile(r'<td title=(.*?)"text-align:center!important;cursor:default;" >', re.S)
        obj2 = re.compile(
            r'<td title="(.*?)" style="text-align:center!important;cursor:default;width:200px!important;text-overflow'
            r':ellipsis;white-space:nowrap;">',
            re.S)
        obj3 = re.compile(r'''onclick="javascript:showDetail\((.*?)\);return''', re.S)
        obj4 = re.compile(r'<td title="(.*?)" style="text-align: center!important;" >')
        obj5 = re.compile(r'<td id="wrap" title="(.*?)"')
        # objend = re.compile(r'''onclick="_gotoPage\('(.*?)'\);">尾页</div>''')
        datas = obj.findall(response.text)
        time.sleep(1)
        for i in datas:
            dict = {}
            dict['xzrmc'] = obj2.findall(i)[0]
            dict['tyshxhdm'] = obj4.findall(i)[0]
            dict['fddbrxm'] = obj4.findall(i)[1]
            dict['cfjdrq'] = obj5.findall(i)[0]
            cleaned_text_list = [text.strip("''") for text in obj3.findall(i)[0].split(',') if text.strip()]
            dict = get_data(cleaned_text_list[0], cleaned_text_list[1], cleaned_text_list[2], dict)
            myset.insert_one(dict)
            logger.info(f'>>>>>>>>>>>>>第{pageNo}页{dict["tyshxhdm"]}导入成功')
    except Exception as e:
        logging.info(f'>>>>>>>>>>>>>>>异常{e}')


pageNo = 1

if pageNo == 1:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://credit.fzgg.tj.gov.cn",
        "Referer": "https://credit.fzgg.tj.gov.cn/xygs/datalist.do",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "sec-ch-ua": "^\\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\\^Windows^^"
    }

    url = "https://credit.fzgg.tj.gov.cn/xygs/datalist.do"
    data = {
        "pageNo": f"{pageNo}",
        "pageSize": "10",
        "messageid": "51BAD61AAD244B499E470ABD8E0EB9DF",
        "domainid": "017",
        "condition": "",
        "paramMap['CF_XDR_MC']": "",
        "paramMap['CF_XDR_SHXYM']": "",
        "paramMap['CF_WSH']": "",
        "paramMap['CF_JDRQ_start']": "",
        "paramMap['CF_JDRQ_end']": "",
        "yzm": ""
    }
    response = requests.post(url, headers=headers, data=data)
    obj = re.compile(r'<td title=(.*?)"text-align:center!important;cursor:default;" >', re.S)
    obj2 = re.compile(
        r'<td title="(.*?)" style="text-align:center!important;cursor:default;width:200px!important;text-overflow'
        r':ellipsis;white-space:nowrap;">',
        re.S)
    obj3 = re.compile(r'''onclick="javascript:showDetail\((.*?)\);return''', re.S)
    obj4 = re.compile(r'<td title="(.*?)" style="text-align: center!important;" >')
    obj5 = re.compile(r'<td id="wrap" title="(.*?)"')
    objend = re.compile(r'''onclick="_gotoPage\('(.*?)'\);">尾页</div>''')

    datas = obj.findall(response.text)
    time.sleep(1)
    for i in datas:
        dict = {}
        dict['szrmc'] = obj2.findall(i)[0]
        dict['tyshxhdm'] = obj4.findall(i)[0]
        dict['fddbrxm'] = obj4.findall(i)[1]
        dict['cfjdrq'] = obj5.findall(i)[0]
        cleaned_text_list = [text.strip("''") for text in obj3.findall(i)[0].split(',') if text.strip()]
        dict = get_data(cleaned_text_list[0], cleaned_text_list[1], cleaned_text_list[2], dict)
        myset.insert_one(dict)
        logger.info(f'>>>>>>>>>>>>>第{pageNo}页{dict["tyshxhdm"]}导入成功')
    max_num = int(objend.findall(response.text)[0])
    logger.info(f'>>>>>>>一共{max_num}页')
    for i in range(2, max_num + 1):
        try:
            get_html(i)
        except Exception as e:
            logging.info(f'>>>>>>>>>>>{i}页异常：{e}')