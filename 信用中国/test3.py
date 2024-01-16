import requests


headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://credit.shandong.gov.cn",
    "Referer": "https://credit.shandong.gov.cn/creditsearch.creditdetailindexbgca.dhtml?entityType=1&kw=913101151324074865&tyshxydm=913101151324074865",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "^\\^Not_A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\\^Windows^^"
}

url = "https://credit.shandong.gov.cn/creditsearch.creditdetalicayth.phtml"
data = {
    "page": "1",
    "type": "行政管理",
    "Category": "credit_xyzx_fr_xzcf_new",
    "kw": "上海锦江出租汽车服务有限公司",
    "call": "2",
    "token": "KbllHRIeLpy7e8LcUQNRKHq2+AuPNEdAM2BEFfkZrI6t6BXibNyRckr04YiiIKQVSNDxE1NMRsvsLnxaRkyIZZlpUpkLXdITT85G639MT1KIL1zCF8p6jmDBA5ItgAyd",
    "timestamp": "1705383535907"
}
response = requests.post(url, headers=headers, data=data)

print(response.text)
print(response)