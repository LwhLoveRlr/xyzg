import requests
import ssl

# 2. 表示忽略未经核实的SSL证书认证
requests.packages.urllib3.disable_warnings()

def get_data(objectId, dict):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://creditbj.jxj.beijing.gov.cn",
        "Referer": "https://creditbj.jxj.beijing.gov.cn/credit-portal/publicity/metadata/record/detail/PUNISH/0"
                   "/D5B461086F20958B0ECC6453DEA49F2F",
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
    url = "https://creditbj.jxj.beijing.gov.cn/credit-portal/api/credit_service/page/detail"
    data = {
        "currentPage": 1,
        "linesPerPage": 2,
        "condition": {
            "publicityTag": "PUNISH",
            "objectType": "0",
            "objectId": objectId
        }
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    if len(response.json()['data']['list']) >= 1:
        for i in response.json()['data']['list']:
            dict['来源'] = i['source']
            dict['来源时间'] = i['time']
            dict['处罚内容'] = 'https://creditbj.jxj.beijing.gov.cn/credit-portal/img_resource'+i['imageUrl']
            return dict

def get_url():

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "Origin": "https://creditbj.jxj.beijing.gov.cn",
        "Referer": "https://creditbj.jxj.beijing.gov.cn/credit-portal/publicity/record/punish_publicity",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    }
    url = "https://creditbj.jxj.beijing.gov.cn/credit-portal/api/publicity/record/PUNISH/0"
    data = {
        "listSql": "",
        "linesPerPage": 10,
        "currentPage": 1,
        "condition": {
            "keyWord": "",
            "openStyle": "2"
        }
    }
    response = requests.post(url, headers=headers, json=data, verify=False)
    dict = {}
    if len(response.json()['data']['list']) > 1:
        for i in response.json()['data']['list']:
            print(i)
            dict['处罚决定书文号'] = i['xzcfjdswh']
            dict['上报部门'] = i['deptName']
            dict['统一社会信用代码'] = i['tyshxydm']
            dict['更新时间'] = i['zhgxsj']
            dict['被处罚单位'] = i['zzmc']
            data = get_data(i['zzbh'], dict)
            print(data)
get_url()