#!/usr/local/bin/ python
# -*- coding: utf-8 -*-


# 配置主机配置文件地址
hostFile = 'host.txt'

# 配置写文件路径
file_path = '../data/'

# 配置用户名和密码
userInfo = {
    'username': 'admin',
    'password': 'xxxxx',

    # 以下两项不需要更改
    'cginame': 'login.cgi',
    'cgiopt': 'get',
}


# 配置短信接收号码
phone_num = {'ph1': '139xxxxxxxx', 'ph2': '139xxxxxxxx'}


# 配置cgi菜单
CgiMem = {
    'system_general': 'systemgeneral.cgi',       # 基本参数
    'system_time': 'systemtime.cgi',             # 时间参数
    'system_network': 'systemnetwork.cgi',       # 网络参数
    'link_Status': 'porte1t1.cgi',               # 链路状态(LOS、LOF、AIS、RIA、SLIP)
    'link_Filter': 'portlink.cgi',               # 链路点码(OPC、DPC、SLC)
    'link_Statis': 'porte1t1statis.cgi',         # 链路统计(MSU)
    'sdtp_Config': 'sdtplinkconfig.cgi',         # SDTP配置
}

# 定义请求头
requestHeader = {
    'Content-Type': 'application/x-www-form-urlencoded',
}


# 配置短信接口参数
SmsInof = {'phone_user' : 'xljc',
           'phone_password' : 'JNpzJzd2',
           'phone_license' : '4c0e00def6fddc5fd8d2ee3521dbd8f7',
           'phone_systeminfo' : '信令监测系统',
           'phone_srctermid' : 2600,
           'phone_url' : 'http://IP:Port/services/SMSService?wsdl',
}


