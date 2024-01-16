import json
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
    query = {"id": dataId}
    result = myset.find_one(query)
    if not result:
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
            response = requests.get(url, headers=headers, params=params)
            data = response.json()['data']['columnShowList']['records'][0]
            # print(f'{data["id"]}保存成功')
            myset.insert_one(data)
            logger.info(f'>>>>>>>>>{data["id"]}保存成功')
        except Exception as e:
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
            response = requests.get(url, headers=headers, params=params)
            html = etree.HTML(response.text)
            verifyId = html.xpath('//input[@id="verifyId"]/@value')[0]
            url = "https://xy.fujian.gov.cn/credit/kk-anti-reptile/refresh"
            params = {
                "verifyId": verifyId
            }
            response1 = requests.post(url, headers=headers, params=params)
            decode_image(response1.json()['verifyImgStr'])
            chaojiying = Chaojiying_Client('15673590950', '031104rlr', '940771')
            im = open('验证码.jpg', 'rb').read()
            img_data = chaojiying.PostPic(im, 1005)
            pic_str = img_data['pic_str']
            url = "https://xy.fujian.gov.cn/credit/kk-anti-reptile/validate"
            params = {
                "verifyId": response1.json()['verifyId'],
                "realRequestUri": "/credit/cmpinternetportalfront/doublepublicity/getPermitList",
                "result": pic_str
            }
            response = requests.post(url, headers=headers, params=params)
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
            response2 = requests.get(url, headers=headers, params=params)
            data = response2.json()['data']['columnShowList']['records'][0]
            myset.insert_one(data)
            logger.info(f'>>>>>>>>>{data["id"]}保存成功')
data_list = []
def get_data(keyword):
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
            "pageSize": "1500",
            "pageNo": 1,
            "keyword": keyword
        }
        response = requests.get(url, headers=headers, params=params)
        time.sleep(1)
        dict = response.json()['data']
        if 'columnShowList' in dict:
            if 'records' in dict['columnShowList']:
                if response.json()['data']['columnShowList']['records']:
                    for records in response.json()['data']['columnShowList']['records']:
                        data_list.append(records['id'])
                else:
                    logging.info('暂无数据')

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
            "pageSize": "1500",
            "pageNo": 1,
            "keyword": keyword
        }
        response = requests.get(url, headers=headers, params=params)
        html = etree.HTML(response.text)
        verifyId = html.xpath('//input[@id="verifyId"]/@value')[0]
        url = "https://xy.fujian.gov.cn/credit/kk-anti-reptile/refresh"
        params = {
            "verifyId": verifyId
        }
        response1 = requests.post(url, headers=headers, params=params)
        decode_image(response1.json()['verifyImgStr'])
        chaojiying = Chaojiying_Client('15673590950', '031104rlr', '940771')
        im = open('验证码.jpg', 'rb').read()
        img_data = chaojiying.PostPic(im, 1005)
        pic_str = img_data['pic_str']
        url = "https://xy.fujian.gov.cn/credit/kk-anti-reptile/validate"
        params = {
            "verifyId": response1.json()['verifyId'],
            "realRequestUri": "/credit/cmpinternetportalfront/doublepublicity/getPermitList",
            "result": pic_str
        }
        response = requests.post(url, headers=headers, params=params)
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
            "pageSize": "1500",
            "pageNo": 1,
            "keyword": keyword
        }
        response1 = requests.get(url, headers=headers, params=params)
        time.sleep(5)
        logging.info('验证成功')
        dict = response.json()['data']

        if 'columnShowList' in dict:
            if 'records' in dict['columnShowList']:
                if response.json()['data']['columnShowList']['records']:
                    for records in response.json()['data']['columnShowList']['records']:
                        data_list.append(records['id'])
                else:
                    logging.info('暂无数据')


all_data = []
with open('output_file.json', 'r', encoding='utf-8') as file:
    data1 = json.load(file)
for i in data1:
    all_data.append(i['LawDepartment'])
all_cities = ['鼓楼区', '台江区', '仓山区', '马尾区', '晋安区', '福清市', '长乐市', '闽侯县', '闽清县', '永泰县', '连江县', '罗源县', '平潭县', '厦门市', '思明区', '海沧区', '湖里区', '集美区', '同安区', '翔安区', '莆田市', '城厢区', '涵江区', '荔城区', '秀屿区', '仙游县', '三明市', '梅列区', '三元区', '永安市', '明溪县', '将乐县', '大田县', '宁化县', '建宁县', '沙县', '尤溪县', '清流县', '泰宁县', '泉州市', '丰泽区', '鲤城区', '洛江区', '泉港区', '石狮市', '晋江市', '南安市', '惠安县', '永春县', '安溪县', '德化县', '金门县', '漳州市', '芗城区', '龙文区', '龙海市', '平和县', '南靖县', '诏安县', '漳浦县', '华安县', '东山县', '长泰县', '云霄县', '南平市', '延平区', '建瓯市', '邵武市', '武夷山市', '建阳市', '松溪县', '光泽县', '顺昌县', '浦城县', '政和县', '龙岩市', '新罗区', '漳平市', '长汀县', '武平县', '上杭县', '永定县', '连城县', '宁德市', '蕉城区', '福安市', '福鼎市', '寿宁县', '霞浦县', '柘荣县', '屏南县', '古田县', '周宁县']
for i in all_data:
    for j in all_cities:
        if j in i:
            logger.info(f'>>>>>>>>>{i}')
            get_data(i)
            time.sleep(0.5)
            break


for data in data_list:
    try:
        query = {"id": data}
        result = myset.find_one(query)
        if not result:
            get_content(data)
            time.sleep(0.5)
    except Exception as e:
        logging.info(e)