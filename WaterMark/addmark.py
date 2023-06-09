#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import sys
import time
import paramiko
import hashlib
import datetime
import logging
import requests
from zeep.client import Client
from collections import OrderedDict


def encrypt_sha256(s):
    '''token加密'''
    m = hashlib.sha256()
    m.update(s.encode("utf8"))
    return m.hexdigest()


class AddMarkWork(object):

    '''
        ftp_url: ftp信息查询调用地址
        mark_url: 加水印调用地址
        status_url: 加水印任务状态查询调用地址
    '''
    # 生产环境
    #ftp_url = 'http://IP:PORT/SHMC/ProxyService/SC/SB_SC_WMS_SH_InquiryFTPAccPwdSrv/SB_SC_WMS_SH_InquiryFTPAccPwdSrv?wsdl'
    #mark_url = 'http://IP:PORT/SHMC/ProxyService/SC/SB_SC_WMS_SH_ImportFileFillWatermarkSrv/SB_SC_WMS_SH_ImportFileFillWatermarkSrv?wsdl'
    #status_url = 'http://IP:PORT/SHMC/ProxyService/SC/SB_SC_WMS_SH_InquiryFileWatermarkStatusSrv/SB_SC_WMS_SH_InquiryFileWatermarkStatusSrv?wsdl'

    # 测试环境
    ftp_url = 'http://IP:PORT/cxf/SB_SC_WMS_SH_InquiryFTPAccPwdSrvPort?wsdl'
    mark_url = 'http://IP:PORT/cxf/SB_SC_WMS_SH_ImportFileFillWatermarkSrvPort?wsdl'
    status_url = 'http://IP:PORT/cxf/SB_SC_WMS_SH_InquiryFileWatermarkStatusSrvPort?wsdl'

    system_id = 'XLJCXT'                                # 系统英文名称
    system_name = '7号信令监测系统'                      # 系统中文名称
    province_code = '021'                               # 省公司代码
    environment_name = 'O'                              # 环境名
    appId = '8237089f-c0ba-4cc3-be17-50a7d55c079b'      # 注册时分配的唯一标识
    securityKey = '4fb1885720c0de684699460ad0a59238'    # key
    remote_path = '/xljcxt'                             # 文件上传路径
    local_path = '/zctt/iaap/service/download'          # 文件本地路径


    def __init__(self):

        self.user_id = ''                               # 用户id
        self.user_name = ''                             # 用户名
        self.timestamp = int(time.time() * 1000)
        self.subtime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.token = 'appId={}&timestamp={}&securityKey={}'.format(AddMarkWork.appId, self.timestamp, AddMarkWork.securityKey)

        # 日志
        self.logger = logging.getLogger('services.export.addmark')

        '''
            定义soap请求数据头和数据实体
            通过colletions.OrderedDict()方法固定请求头和请求体参数顺序
        '''
        # 构建请求头
        self.msgheader = OrderedDict()
        self.msgheader['SOURCESYSTEMID'] = AddMarkWork.system_id
        self.msgheader['SOURCESYSTEMNAME'] = AddMarkWork.system_name
        self.msgheader['USERID'] = self.user_id
        self.msgheader['USERNAME'] = self.user_name
        self.msgheader['SUBMITDATE'] = self.subtime
        self.msgheader['PAGE_SIZE'] = 50
        self.msgheader['CURRENT_PAGE'] = 1
        self.msgheader['TOTAL_RECORD'] = 50
        self.msgheader['PROVINCE_CODE'] = AddMarkWork.province_code
        self.msgheader['ENVIRONMENT_NAME'] = AddMarkWork.environment_name

        # 构建请求体
        self.request_Body = OrderedDict()
        self.request_Body['APP_ID'] = AddMarkWork.appId
        self.request_Body['TOKEN'] = encrypt_sha256(self.token)
        self.request_Body['TIMESTAMP'] = self.timestamp


    def query_ftp_info(self):
        '''获取ftp信息'''
        try:
            ftp_client = Client(AddMarkWork.ftp_url)
            logging.info(ftp_client)
            ret_info = ftp_client.service.process(self.msgheader, *self.request_Body.values())
            print(ret_info)
            self.ftp_info = {'ErrorFlag': ret_info['ErrorFlag'],
                             'ip': ret_info['HOST'],
                             'user': ret_info['FTP_USER_NAME'],
                             'pwd' : ret_info['FTP_USER_PWD']
            }
            return self.ftp_info
        except requests.exceptions.ConnectionError as error:
            self.logger.info('Error: %s' % error)
            return None


    def sftp_file(self, sftp_key, file_name):
        '''上传和下载文件'''
        try:
            t = paramiko.Transport((self.ftp_info['ip'], 22))
            t.connect(username=self.ftp_info['user'], password=self.ftp_info['pwd'])
            sftp = paramiko.SFTPClient.from_transport(t)

            sftp.chdir('.' + AddMarkWork.remote_path)

            if sftp_key == 'put':
                self.logger.info('>>>>>>正在上传文件 {}.xls<<<<<<'.format(file_name))
                sftp.put(AddMarkWork.local_path + '/' + file_name + '.xls', file_name + '.xls')
                self.logger.info('>>>>>>上传文件成功 {}.xls<<<<<<'.format(file_name))
            else:
                self.logger.info('>>>>>>正在下载文件 %s<<<<<<' % self.path.split('/')[-1])
                sftp.get(self.path.split('/')[-1], AddMarkWork.local_path + '/' + file_name + '.xls')

            t.close()
            return True

        except Exception as e:
            self.logger.error(e)
            return False


    def get_FileFillWater(self, file_name):
        '''提交文件水印'''
        self.file_size = os.path.getsize(AddMarkWork.local_path + '/' + file_name + '.xls')

        body_dict = OrderedDict()
        body_dict['CONTENT'] = ' '.join([self.user_name, self.subtime])
        body_dict['USER_NAME'] = '' # 待补充
        body_dict['LOGIN_NAME'] = self.user_name
        body_dict['DEPT_NAME'] = '' # 待补充
        body_dict['FILE_NAME'] = '.'.join([file_name, 'xls'])
        body_dict['FILE_TYPE'] = '话单'
        body_dict['FILE_SIZE'] = self.file_size
        body_dict['SRC_FORMAT'] = 'xls'
        body_dict['TARGET_FORMAT'] = 'xls'
        body_dict['BUSINESS_KEY'] = ''
        body_dict['REQUEST_REMARK'] = ''
        body_dict['HOST'] = self.ftp_info['ip']
        body_dict['PATH'] = AddMarkWork.remote_path + '/' + file_name + '.xls'
        body_dict['CONVERTER'] = ''
        body_dict['CAN_MODIFY'] = 'Y'
        body_dict['MODIFY_PWD'] = ''
        body_dict['CAN_PRINT'] = 'Y'
        body_dict['CAN_OPEN'] = 'Y'
        body_dict['OPEN_PWD'] = ''

        Water_client = Client(AddMarkWork.mark_url)
        self.request_Body.update(body_dict)
        ret_info = Water_client.service.process(self.msgheader, *self.request_Body.values())
        self.logger.info(ret_info)

        self.trans_no = ret_info['TRANS_NO']
        return self.trans_no


    def get_WaterStatus(self):
        '''获取文件加水印状态'''
        status_client = Client(AddMarkWork.status_url)
        # 构建请求体
        self.request_Body['TRANS_NO'] = self.trans_no
        keys = ['APP_ID', 'TOKEN', 'TIMESTAMP', 'TRANS_NO']
        temp_data_list = [self.request_Body[k] for k in keys]
        # 请求接口信息
        ret_info = status_client.service.process(self.msgheader, *temp_data_list)
        self.logger.info(ret_info)
        # 返回文件加水印状态和远程路径
        status, self.path = ret_info['RESULTS_LIST']['RESULTS_ITEM'][0]['STATUS'], ret_info['RESULTS_LIST']['RESULTS_ITEM'][0]['PATH']
        self.logger.info('文件加水印状态 >>> status: %s, path: %s' %(status, self.path))

        return status, self.path

        
