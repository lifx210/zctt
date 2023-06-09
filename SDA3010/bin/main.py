#!/usr/local/bin/ python
# -*- coding: utf-8 -*-


import os
import sys
import json
import pyodbc
import logging
import subprocess
import requests
import threading
from datetime import datetime
from SdaClass import SDA_class
from sms_encapsulation import Encap_Sms
from setting import hostFile, file_path, userInfo, requestHeader


# 定义输出日志
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s - %(name)s - %(filename)s,line:%(lineno)d - %(levelname)s] %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S %a',
                    filename='../log/sda.log',
                    filemode='a',
                    )


# 定义时间和写文件名
local_time = datetime.now()
time_str = datetime.strftime(local_time, '%Y%m%d%H%M')
start_time = datetime.strftime(local_time, '%Y-%m-%d %H:%M')
file_name = 'sdainfo_' + time_str + '.dat'
db_name = 'monitor'
table_name = 'noc_sda'


def InsertMsg(msg, db_name, table_name):
    '''数据入库'''
    try:
        conn = pyodbc.connect('DSN=' + db_name)
        cousor = conn.cursor()
        sql ='''insert into %s (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) values(%s);'''%(
            table_name,
            'start_time', 
            'manageIp', 
            'bussIp', 
            'linkNum', 
            'linkStat', 
            'linkAlm', 
            'opc', 
            'dpc', 
            'slc', 
            'msupck', 
            'msubyte', 
            'msudrop', 
            'crcerr',
            msg)
        cousor.execute(sql)
        cousor.commit()
    except Exception as error:
        logging.error('Mysql Error: {}'.format(error))
    finally:
        if 'conn' in dir():
            conn.close()


def GetSdaInfo(RequestUrl, ip, url, sessionid):
    '''通过Class类获取每一项指标'''
    sdaObjetc = SDA_class(RequestUrl, ip, url, sessionid, requestHeader)
    # system_general_list = sdaObjetc.system_general()
    # system_time_list = sdaObjetc.system_time()
    # sdtp_Config_list = sdaObjetc.sdtp_Config()
    system_network_list = sdaObjetc.system_network()
    link_Status_list = sdaObjetc.link_Status()
    link_Filter_list = sdaObjetc.link_Filter()
    link_Statis_list = sdaObjetc.link_Statis()
    link_Info = list(zip(link_Status_list, link_Filter_list, link_Statis_list))

    # 写文件和入库
    with open(file_path + file_name, 'a') as f:
        for row in link_Info:
            msgInfo = '|'.join(system_network_list + row[0] + row[1] + row[2])
            f.write(msgInfo + '\n')
            # 入库进程
            InsertMsg("'{}','".format(start_time) + msgInfo.replace('|', "','") + "'", db_name, table_name)
    f.close()


def RequestUrl(url, reqHeader, reqBody):
    '''请求url'''
    try:
        response_str = requests.post(url, headers=reqHeader, data=reqBody)
        response_json = json.loads(response_str.text.split('\n')[1].strip())
    except requests.exceptions.ConnectionError as error:
        response_json = {}
    return response_json


def getLoginSessionId(ip, url):
    '''获取用户登录后的session ID'''
    response_json = RequestUrl(url, requestHeader, userInfo)
    if response_json != {}:
        sessionid = response_json['sessionid']
        logging.info(' >>> '.join([ip, 'Login Session ID: ' + sessionid]))
        # 获取SDA各项指标
        GetSdaInfo(RequestUrl, ip, url, sessionid)
    else:
        logging.error(' >>> '.join([ip, 'Connect Fild!']))

        '''
        此处告警触发存在问题，待排查
        '''
        smsSend.perfect_sms('[SmsServer:10.221.231.68]: The SDA %s Web Connect Fild!' %(ip))


def CheckIp(ip):
    '''检测ip状态'''
    ret = subprocess.getstatusoutput('ping -c 1 ' + ip)
    if ret[0] == 0:
        statusCode = 1
    else:
        statusCode = -1
    return statusCode


def ReadFile(file_name):
    '''读取主机配置文件'''
    ip_list = []
    with open(file_name, 'r') as f:
        for row in f.readlines():
            ip = row.strip()
            statusCode = CheckIp(ip)
            if statusCode == 1:
                ip_list.append(ip)
            else:
                logging.error(ip + ' >>> Down')
                smsSend.perfect_sms('[SmsServer:10.221.231.68]: The SDA %s is Down!' %(ip))
    return ip_list


def main():
    '''主函数'''

    global ip_list
    if os.path.exists(hostFile):
        ip_list = ReadFile(hostFile)
    else:
        logging.error('Host Config File not exits, The Program Exit!!!')
        sys.exit()

    for ip in ip_list:
        url = os.path.join('http://', ip, 'cgi-bin', 'www.cgi')
        t1 = threading.Thread(target=getLoginSessionId, args=(ip, url))
        t1.start()
        t1.join()

    logging.info('WriteFileName >>> [{}]'.format(os.path.abspath(file_name)))


if __name__ == '__main__':
    reload(sys)                                 
    sys.setdefaultencoding( "utf-8" )
    smsSend = Encap_Sms()
    main()
