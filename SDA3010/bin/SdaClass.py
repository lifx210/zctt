#!/usr/local/bin/ python
# -*- coding: utf-8 -*-


import logging
from setting import CgiMem
from sms_encapsulation import Encap_Sms


# 定义输出日志
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s - %(name)s - %(filename)s,line:%(lineno)d - %(levelname)s] %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S %a',
                    filename='../log/sda.log',
                    filemode='a',
                    )

smsSend = Encap_Sms()


class SDA_class(object):

    def __init__(self, RequestUrl, ip, url, sessionid, requestHeader):
        self.RequestUrl = RequestUrl
        self.ip = ip
        self.url = url
        self.sessionid = sessionid
        self.requestHeader = requestHeader


    def create_requestBody(self, cginame):
        '''构建请求体'''
        request_body = {
            'sessionid': self.sessionid,
            'cginame': cginame,
            'cgiopt': 'get',
        }
        return request_body


    def system_general(self):
        '''获取基本数据'''
        request_body = self.create_requestBody(CgiMem['system_general'])
        logging.info(' >>> '.join([self.ip, 'Reuqest Body: ' + str(request_body)]))
        system_general_json = self.RequestUrl(self.url, self.requestHeader, request_body)
        logging.info(' >>> '.join([self.ip, 'System General Json: ' + str(system_general_json)]))
        cpuusage = system_general_json['cpuusage']
        memusage = system_general_json['memusage']
        diskusage = system_general_json['diskusage']
        data = [cpuusage, memusage, diskusage]
        return data


    def system_time(self):
        '''获取ntp数据'''
        request_body = self.create_requestBody(CgiMem['system_time'])
        logging.info(' >>> '.join([self.ip, 'Reuqest Body: ' + str(request_body)]))
        system_time_json = self.RequestUrl(self.url, self.requestHeader, request_body)
        logging.info(' >>> '.join([self.ip, 'System Time Json: ' + str(system_time_json)]))
        ntpsrvip = system_time_json['ntpsrvip']
        data = [ntpsrvip]
        return data


    def system_network(self):
        '''获取网络数据'''
        request_body = self.create_requestBody(CgiMem['system_network'])
        logging.info(' >>> '.join([self.ip, 'Reuqest Body: ' + str(request_body)]))
        system_network_json = self.RequestUrl(self.url, self.requestHeader, request_body)
        logging.info(' >>> '.join([self.ip, 'System Network Json: ' + str(system_network_json)]))
        manageIp = system_network_json['ip0']
        bussIP = system_network_json['ip1']
        # maskIp = system_network_json['mask1']
        # getwayIp = system_network_json['gateway0']
        # manageMac = system_network_json['mac0']
        # bussMac = system_network_json['mac1']
        # data = [manageIp, bussIP, maskIp, getwayIp, manageMac, bussMac]
        data = [manageIp, bussIP]
        return data


    def link_Status(self):
        '''获取E1链路状态'''
        data = []
        request_body = self.create_requestBody(CgiMem['link_Status'])
        logging.info(' >>> '.join([self.ip, 'Reuqest Body: ' + str(request_body)]))
        i = 0
        while i < 8:
            request_body['chanidx'] = i
            link_num = str(i + 1)
            link_Status_json = self.RequestUrl(self.url, self.requestHeader, request_body)
            logging.info(' >>> '.join([self.ip, 'Link Status Json: ' + str(link_Status_json)]))
            ret = link_Status_json['chansta']
            n = 0
            link_status = 'normal'
            link_alm = []
            while n < 5:
                if list(ret.items())[n][1] == 'alarm':
                    link_status = 'alarm'
                    link_alm.append(list(ret.items())[n][0][:3].upper())
                    if n == 3:
                        self.Sms_List.append('SDA {} [linkNum:{} >>> linkAlm:{}]'.format(self.ip, link_num, '_'.join(link_alm).upper()))
                n += 1
            link_alm = '_'.join(link_alm)
            data.append([link_num, link_status, link_alm])
            i += 1
        return data


    def link_Filter(self):
        '''获取E1链路点码'''
        data = []
        request_body = self.create_requestBody(CgiMem['link_Filter'])
        logging.info(' >>> '.join([self.ip, 'Reuqest Body: ' + str(request_body)]))
        link_Filter_json = self.RequestUrl(self.url, self.requestHeader, request_body)
        logging.info(' >>> '.join([self.ip, 'Link Filter Json: ' + str(link_Filter_json)]))
        ret = link_Filter_json['linkresult']['rows']
        i = 0
        while i < len(ret):
            data.append(ret[i]['cell'][-3:])
            i += 1
        return data


    def link_Statis(self):
        '''获取链路数据包'''
        data = []
        request_body = self.create_requestBody(CgiMem['link_Statis'])
        logging.info(' >>> '.join([self.ip, 'Reuqest Body: ' + str(request_body)]))
        link_Statis_json = self.RequestUrl(self.url, self.requestHeader, request_body)
        logging.info(' >>> '.join([self.ip, 'Link Statis Json: ' + str(link_Statis_json)]))
        msupckList = link_Statis_json['msupck']
        msubyteList = link_Statis_json['msubyte']
        msudropList = link_Statis_json['msudrop']
        crcerrList = link_Statis_json['crcerr']
        StatisList = list(zip(msupckList, msubyteList, msudropList, crcerrList))
        i = 0
        while i < len(StatisList):
            data.append(list(StatisList[i]))
            i += 1
        return data


    def sdtp_Config(self):
        '''获取SDTP配置'''
        request_body = self.create_requestBody(CgiMem['sdtp_Config'])
        logging.info(' >>> '.join([self.ip, 'Reuqest Body: ' + str(request_body)]))
        sdtp_Config_json = self.RequestUrl(self.url, self.requestHeader, request_body)
        logging.info(' >>> '.join([self.ip, 'Sdtp Config Json: ' + str(sdtp_Config_json)]))
        sdtpServer = sdtp_Config_json['ipaddr']
        sdtpPort = sdtp_Config_json['desport']
        data = [sdtpServer, sdtpPort]
        return data

