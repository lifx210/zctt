#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import base64
import requests


# 配置短信接收号码
phone_num = {'ph1' : '139xxxxxxx',
             'ph2' : '139xxxxxxx',
}


# 配置短信接口参数
SmsInof = {'phone_user' : 'xljc',
           'phone_password' : 'J****2',
           'phone_license' : '4c0e00****bd8f7',
           'phone_systeminfo' : '信令监测系统',
           'phone_srctermid' : 2600,
           'phone_url' : 'http://IP:Port/services/SMSService?wsdl',
}


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

    def __init__(self, phone_msgcontent):
        self.phone_msgcontent = phone_msgcontent
        # if len(sys.argv) > 1:
        #     self.phone_msgcontent = sys.argv[1]
        # else:
        #     self.phone_msgcontent = phone_msgcontent

    def perfect_sms(self, **kwargs):
        for ph in phone_num.values():
            messages_xml = sms_xml.format(phone=ph, msgcontent=self.phone_msgcontent, **SmsInof)
            jm_xml_str = base64.b64encode(messages_xml.encode()).decode('utf-8')

            # 请求SmsSendMQ方法
            RequestData = {
                'url': SmsInof['phone_url'],
                'data': SendMQ_xml.format(jm_xml_str),
                'headers': SendMQ_request_head
            }
            response = requests.post(**RequestData)
            print(response.json)


