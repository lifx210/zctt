#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import pyodbc
import datetime
import logging


# 定义输出日志
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(filename)s[%(lineno)d] %(levelname)s：%(message)s",
                    datefmt = '%Y-%m-%d %H:%M:%S %a',
                    filename = 'secret.log',
                    filemode = 'a'
                    )


# 定义当前时间、创建文件时间
now_time = datetime.datetime.now()
files_day_int = datetime.datetime.strftime(now_time + datetime.timedelta(hours=-1), '%Y%m%d%H')
creat_files_day = files_day_int[:8]
creat_files_hour = files_day_int[-2:]


# 定义日志固定字段值
app_server_anme = '7号信令监测系统'
filename_sysname = '7号信令监测系统'
app_server_ip = 'IP'
sensitive_name = '开始通信时间,时长,流量,上网日志,地区代码'
sensitive_code = 'C1-2,C1-4'
system_number = '122'
city_name = '上海移动'
operation_types = {'select' : '4',
                  'download' : '10',
                  'login' : '12',
                  'logout' : '13',
                  'other' : '5'
}


# 定义其他
start_time_str = ''
end_time_str = ''
logs_list =[]

# 定义数据库和日志表
table_name = 'st_operationlog'
db_name = ['monitor']


class Select_info(object):

    def __init__(self, now_time, start_time_str, end_time_str, table_name, db_name):

        self.now_time = now_time
        self.start_time_str = start_time_str
        self.end_time_str = end_time_str
        self.table_name = table_name
        self.db_name = db_name

    def select_time(self):
        '''输出查询开始结束时间'''

        h = self.now_time.hour
        m = self.now_time.minute
        s = self.now_time.second

        start_time = self.now_time + datetime.timedelta(hours=-1, minutes=-m, seconds=-s)
        self.start_time_str = start_time.__str__().split('.')[0]
        end_time = self.now_time + datetime.timedelta(minutes=-m, seconds=-s)
        self.end_time_str = end_time.__str__().split('.')[0]

        return self.start_time_str, self.end_time_str

    def select(self):
        '''查询日志表'''

        try:
            conn = pyodbc.connect('DSN=' + self.db_name)
            cousor = conn.cursor()
            sql ='''select %s, %s, %s, %s, %s, %s, %s, %s from %s where operationtime >= '%s' and operationtime <= '%s';'''\
                 %('logid', 'operation', 'functionname', 'description','username', 'operationtime',
                   'opresult','loginip', self.table_name, self.start_time_str, self.end_time_str)
            cousor.execute(sql)
            rows = cousor.fetchall()
            for row in rows:
                logs_list.append(row)
            cousor.commit()
        except Exception as error:
            print(error)
        finally:
            if 'conn' in dir():
                conn.close()
        return logs_list


def get_menu(*args):
    '''输出查询菜单'''

    if operation == '登录' and functionname == 'Authorization':
        menu = '登入系统'
        operation_type = operation_types['login']
    elif operation == '登录' and functionname == '登录':
        menu = description.strip('.')
        operation_type = operation_types['login']
    elif operation == 'Logout':
        menu = '登出系统'
        operation_type = operation_types['logout']
    elif operation == '导出':
        menu = functionname.split('>>>')[-1].strip()
        operation_type = operation_types['download']
    elif operation == '查询' and '>>>' in functionname:
        menu = functionname.split('>>>')[-1].strip()
        operation_type = operation_types['select']
    else:
        menu = functionname
        operation_type = operation_types['select']
    return menu, operation_type


def get_workno(description):
    '''输出工单号和工单类型'''

    if description.find('SH') != -1:
        WorkNo = description.split('}{')[-2].split('=')[-1]
        sheetType = WorkNo.split('-', 2)[1]
        if sheetType.startswith('0'):
            sheetType = sheetType.strip('0')
        else:
            sheetType = sheetType
        return WorkNo, sheetType


if __name__ == '__main__':
    '''程序入口'''

    logs = Select_info(now_time, start_time_str, end_time_str, table_name, db_name[0])
    logs.select_time()
    local_path = os.getcwd()
    jinku_dir = local_path + '/jinku/'
    mingan_dir = local_path + '/mingan/'
    nomingan_dir = local_path + '/nomingan/'
    for x in (jinku_dir, mingan_dir, nomingan_dir):
        if x in os.listdir(os.getcwd()):
            pass
        else:
            os.system('mkdir -p ' + x)

    with open(mingan_dir + '10200_CS_mingan_' + creat_files_day + '_' + creat_files_hour + '.txt', 'a+') as f1, \
            open(jinku_dir + 'i_10200_CS_jinku_' + creat_files_day + '_' + creat_files_hour + '.txt', 'a+') as f2, \
            open(nomingan_dir + '10200_CS_nomingan_' + creat_files_day + '_' + creat_files_hour + '.txt', 'a+') as f3:
        for x in logs.select():
            logid = x[0]
            operation = x[1]
            functionname = x[2]
            description = x[3]
            username = x[4]
            s_time = datetime.datetime.strftime(x[5], '%Y%m%d%H%M%S')
            temp_time = x[6]
            loginip = x[-1]
            menu = get_menu(operation, functionname, description)[0]
            operation_type = get_menu(operation, functionname, description)[1]
            workno = get_workno(description)
           
            if description.find('SH') != -1:
                e_time = int(s_time) + 1
                mingan_touble = (logid,username, username, '00', system_number, '0', app_server_ip, loginip,
                                 s_time, '4', menu, sensitive_name, sensitive_code, '3', '1', '工单',  workno[0])

                jinku_touble = (logid, app_server_anme, system_number, username, '02', '', city_name, filename_sysname,
                                '工单', workno[1], workno[0], s_time, str(e_time), '0', workno[0], '00,02', '', '')

                jinku = '|'.join(jinku_touble)
                mingan = '|'.join(mingan_touble)
                f1.write(mingan + '\n')
                f2.write(jinku + '\n')
                logging.info(jinku)
                logging.info(mingan)

            else:
                nomingan_touble = (logid,username, username, '00', system_number, '0', app_server_ip,
                                   loginip, s_time, operation_type, menu)

                nomingan = '|'.join(nomingan_touble)
                f3.write(nomingan + '\n')
                logging.info(nomingan)
