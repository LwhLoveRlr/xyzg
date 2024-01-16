# -*- coding: UTF-8 -*-
import time

import execjs
import requests


def get_content(kw, page):
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
        "kw": kw,
        "token": token,
        "timestamp": timestamp,
        'page': page,
        'type': '行政管理',
        # 'call': 2
    }
    response = requests.post(url, headers=headers, params=params)
    for i in response.json()['typeSourceSearch']['list']:
        print(i)
    if page == 1:
        max_num = int(response.json()['typeSourceSearch']['total'])
        num = int(max_num / 10)
        if num % 10 != 0:
            num += 1
        for j in range(2, num + 1):
            print(page)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            page += 1
            get_content(kw, num)


def get_kw(kw):
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
    get_content(kw1, page)


def get_my(page):
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


for i in range(1, 51):
    get_my(i)
