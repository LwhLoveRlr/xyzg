import time

import execjs
import requests


# ** 获取第二层的数据
# 加密参数token
# 加密方式：sd.js => get_token() 函数
# 将获取的到的第一层（公司名称）进行加密
# 获取token值
# #
def get_content(kw, page):
    print(page)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
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
        for j in range(2, num+1):
            page += 1
            get_content(kw, num)
kw = "上海锦江出租汽车服务有限公司"
get_content(kw, 1)