# -*- coding: UTF-8 -*-
import logging
import sys
import time

from mongo_config import generate_mongo_conn
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
myset = mongodb_laws_2023['xyzg_jxi']

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


list = ['D0D5B72C4D4AFEC15694DEBC6E10767C', '76BAACBF12EE9319C7D8807C157E3A3A', 'CECFD64406EFD4D2107DD373546EBBB8', 'ABB7D6D22B303EF5944B85B1845A445E', '567B81DF661EBD8DEDC4B5FCC5770A49', 'E490016CB9A33A1667C6E623A55CC947', 'A5B4FF957FF21DF4589332F9211B0AA1', '397F7F02E0DDA504CA7C13EEE9466801', 'CFBFE3FE92463058E1386203DEF894A6', '71775DD877549B186A3A1F1CC4AA996A', '9AD2BC2EDF7AF09EADB5C3EBB1478625', 'D206D1C2F31C99B5EADD7E40D26A3A61', '6CD8C9720749A1AA761123A622C0CD2D']

def get_content(unid):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://zffw.jxzwfww.gov.cn",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    url1 = "http://zffw.jxzwfww.gov.cn/xzzf/api/sendRequest/sendRequest"
    data1 = {
        "url": "http://10.4.13.11:20020/lwpro-security//api/power/powerDetails",
        "unid": unid
    }
    response1 = requests.post(url1, headers=headers, data=data1, verify=False)
    dict = {}
    powerEntity = response1.json()['powerEntity']
    dict['code'] = powerEntity['code'] #职权编号
    dict['createtime'] = powerEntity['createtime']#创建时间
    dict['deptName'] = powerEntity['deptName'] #所属单位
    dict['deptUnid'] = powerEntity['deptUnid']#所属单位id
    dict['dutyLeader'] = powerEntity['dutyLeader'] #责任领导
    dict['dutyOffice'] = powerEntity['dutyOffice'] #责任科室(岗位)
    dict['handlestate'] = powerEntity['handlestate']# 处理结果
    dict['lawlimitDay'] = powerEntity['lawlimitDay']# 法定期限
    dict['name'] = powerEntity['name']  #职权名称
    dict['publicStyle'] = powerEntity['publicStyle'] #公开类型
    dict['superviseTelephone'] = powerEntity['superviseTelephone'] #监督电话
    dict['telephone'] = powerEntity['telephone']
    dict['timestamp'] = powerEntity['timestamp']#时间戳
    dict['type'] = powerEntity['type'] #职权类型
    dict['unid'] = powerEntity['unid'] #id
    dict['version'] = powerEntity['version']#版本
    myset.insert_one(dict)
    logger.info(f'>>>>>>>>>>>>>>>>{dict["unid"]}保存成功')

def get_data(page, deptUnid):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://zffw.jxzwfww.gov.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://zffw.jxzwfww.gov.cn/xzzf/web/infoShow/power/powerList.html?menuId=menu_a_1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    cookies = {
        "BIGipServerliangfaxianjie": "101516298.13390.0000"
    }
    url = "http://zffw.jxzwfww.gov.cn/xzzf/api/sendRequest/sendRequest"
    data = {
        "url": "http://10.4.13.11:20020/lwpro-security//api/power/powerList",
        "deptUnid": deptUnid,
        "page": page,
        "limit": "10",
        "name": "",
        "code": ""
    }
    response = requests.post(url, headers=headers, cookies=cookies, data=data, verify=False)
    for powerList in response.json()['powerList']:
        try:
            get_content(powerList['unid'])
        except Exception as e:
            time.sleep(5)
            logging.info(e)


def get_one(deptUnid):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://zffw.jxzwfww.gov.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://zffw.jxzwfww.gov.cn/xzzf/web/infoShow/power/powerList.html?menuId=menu_a_1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "http://zffw.jxzwfww.gov.cn/xzzf/api/sendRequest/sendRequest"
    data = {
        "url": "http://10.4.13.11:20020/lwpro-security//api/power/powerList",
        "deptUnid": deptUnid,
        "page": "1",
        "limit": "10",
        "name": "",
        "code": ""
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    for powerList in response.json()['powerList']:
        get_content(powerList['unid'])

    max_num = int(response.json()['total'])
    num = int(max_num / 10)
    if num % 10 != 0:
        num += 1
    print(max_num, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    for i in range(2, num + 1):
        try:
            get_data(i, deptUnid)
        except Exception as e:
            time.sleep(5)
            logging.info(f'>>>>>>>>>>>>>>>异常{e}')
def get_all_id(deptUnid):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://zffw.jxzwfww.gov.cn",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "http://zffw.jxzwfww.gov.cn/xzzf/api/sendRequest/sendRequest"
    data = {
        "url": "http://10.4.13.11:20020/lwpro-security//api/ucapDept/regonList",
        "deptUnid": deptUnid
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    list_data1 = []
    for regonList in response.json()['regonList']:
        list_data1.append(regonList['deptUnid'])
    # print(list_data1)
    return list_data1
for id in range(0,len(list)):
    if id == 0 or id == 12:
        try:
            get_one(list[id])
        except Exception as e:
            time.sleep(5)
            logging.info(f'>>>>>>>>>>>>>>>异常{e}')
    else:
        all_list = get_all_id(list[id])
        for all in all_list:
            try:
                get_one(all)
            except Exception as e:
                time.sleep(5)
                logging.info(f'>>>>>>>>>>>>>>>异常{e}')