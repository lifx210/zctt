#!/usr/local/bin/ python
# -*- coding: utf-8 -*-


import re
import base64
import requests
from setting import phone_num, SmsInof


# 配置XML模板
sms_xml = '''<?xml version='1.0' encoding='UTF-8'?>
                <xml>
                <message>
                <OneRecord>
                <desttermid>{phone}</desttermid>
                <username>{phone_user}</username>
                <password>{phone_password}</password>
                <licence>{phone_license}</licence>
                <msgcontent><![CDATA[{msgcontent}]]></msgcontent>
                <systeminfo><![CDATA[{phone_systeminfo}]]></systeminfo>
                <srctermid>{phone_srctermid}</srctermid>
                </OneRecord>
                </message>
                </xml>'''


# 配置SmsSendMQ请求头
SendMQ_request_head = {
  'content-type': 'text/xml',
  'charset': 'UTF-8',
  'SOAPAction': 'urn:SmsSendMQ'
}


# 配置SmsSendMQ请求体
SendMQ_xml = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:axis="http://ws.apache.org/axis2">
                    <soapenv:Body>
                        <axis:SmsSendMQ>
                            <xmlString>{}</xmlString>
                        </axis:SmsSendMQ>
                    </soapenv:Body>
                </soapenv:Envelope>'''


class Encap_Sms(object):

    def perfect_sms(self, phone_msgcontent, **kwargs):
        '''短信接口'''
        for ph in phone_num.values():
            messages_xml = sms_xml.format(phone=ph, msgcontent=phone_msgcontent, **SmsInof)
            jm_xml_str = base64.b64encode(messages_xml)

            # 请求SmsSendMQ方法
            RequestData = {
                'url': SmsInof['phone_url'],
                'data': SendMQ_xml.format(jm_xml_str),
                'headers': SendMQ_request_head
            }
            response = requests.post(**RequestData)
            
            # 获取请求结果状态码
            # resultCode = re.findall('<return>\d</return>', response.text)[0]

