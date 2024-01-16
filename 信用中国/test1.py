import time

import requests
import execjs

#** 获取第一层的数据
# 加密参数token
# 加密方式：sd.js => get_token() 函数
# 将获取的response.json()['baseinfo']['data']['headEntity']['jgmc']  （公司名称）
# #


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Origin": "https://credit.shandong.gov.cn",
    "Pragma": "no-cache",
    "Referer": "https://credit.shandong.gov.cn/creditsearch.creditdetailindexbgca.dhtml?entityType=1&kw=91371524673171488G&tyshxydm=91371524673171488G",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "^\\^Not.A/Brand^^;v=^\\^8^^, ^\\^Chromium^^;v=^\\^114^^, ^\\^Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\\^Windows^^"
}
url = "https://credit.shandong.gov.cn/creditsearch.creditdetalicayth.phtml"
kw = "91371524673171488G"
timestamp = int(time.time()*1000)
token = execjs.compile(open('sd.js', encoding='utf-8').read()).call('get_token', kw, timestamp)
params = {
    "call": "1",
    "kw": kw,
    "token": token,
    "timestamp": timestamp,
    "tyshxydm": kw
}
response = requests.post(url, headers=headers, params=params)
print(response.json()['baseinfo']['headEntity']['jgmc'])
