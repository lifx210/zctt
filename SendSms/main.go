package main

import (
	"bytes"
	"encoding/base64"
	"encoding/xml"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

// 定义常量
const (
  smsUrl = "http://IP:PORT/services/SMSService?wsdl"
	xmlHeader  = `<?xml version='1.0' encoding='UTF-8'?>` + "\n"
	username   = "xljc"
	password   = "J****2"
	srctermid  = 2600
	systeminfo = "信令监测系统"
	licence    = "4c0e****d8f7"
)

// 定义请求xml结构体
type ReqXml struct {
	XMLName xml.Name `xml:"xml"`
	Message messager `xml:"message"`
}

type messager struct {
	OneRecord OneRecorder `xml:"OneRecord"`
}

type OneRecorder struct {
	Desttermid string `xml:"desttermid"`
	Username   string `xml:"username"`
	Password   string `xml:"password"`
	Licence    string `xml:"licence"`
	Msgcontent CDATA  `xml:"msgcontent"`
	Systeminfo CDATA  `xml:"systeminfo"`
	Srctermid  int64  `xml:"srctermid"`
}

type CDATA struct {
	string `xml:",cdata"`
}

// 定义SmsSendMQ方法中xml结构体
type Enveloper struct {
	XMLName xml.Name `xml:"soapenv:Envelope"`
	Xmlns1  string   `xml:"xmlns:soapenv,attr"`
	XMlns2  string   `xml:"xmlns:axis,attr"`
	Bodys   Bodyer   `xml:"soapenv:Body"`
}

type Bodyer struct {
	SmsSendMQs SmsSendMQer `xml:"axis:SmsSendMQ"`
}

type SmsSendMQer struct {
	XMLString string `xml:"xmlString"`
}

// 构建命令行flag参数
func flagInfo() (phonestr, alarmstr string) {
	// 定义参数数据类型
	var Alarm, phone string

	flag.StringVar(&phone, "p", "", "Alarm Phone Number")
	flag.StringVar(&Alarm, "f", "", "Alarm Messages")
	flag.Parse()
	return phone, Alarm
}

// 结构体构建函数,返回请求xml的结构体指针
func newXml(phoneNum, alarmmsg string) *ReqXml {
	return &ReqXml{
		Message: messager{
			OneRecord: OneRecorder{
				Desttermid: phoneNum,
				Username:   username,
				Password:   password,
				Licence:    licence,
				Msgcontent: CDATA{alarmmsg},
				Systeminfo: CDATA{systeminfo},
				Srctermid:  srctermid,
			},
		},
	}
}

func sendMq(s *string) (sendXml []byte) {
	sendXmler := Enveloper{
		Xmlns1: "http://schemas.xmlsoap.org/soap/envelope/",
		XMlns2: "http://ws.apache.org/axis2",
		Bodys: Bodyer{
			SmsSendMQs: SmsSendMQer{
				XMLString: *s,
			},
		},
	}
	sendXml, err := xml.MarshalIndent(sendXmler, " ", " ")
	if err != nil {
		panic(err)
	}
	return
}

func SmsSendMQ(requestType string, requestBody []uint8) (resultCode string) {

	// 构建request对象
	request, err := http.NewRequest(requestType, smsUrl, bytes.NewBuffer(requestBody))
	if err != nil {
		panic(err)
	}
	// 设置POST请求的头
	request.Header.Set("SOAPAction", "urn:SmsSendMQ")
	request.Header.Set("Content-Type", "text/xml")
	request.Header.Set("charset", "utf-8")

	// 创建http请求的客户端对象
	client := &http.Client{}
	responce, err := client.Do(request)
	defer responce.Body.Close()
	if err != nil {
		panic(err)
	}

	data, _ := ioutil.ReadAll(responce.Body)
	resultCode = string(data[215:216])
	fmt.Printf("resultCode: %s \n", resultCode)
	return
}

// XML进行Base64加密函数
func xmlTEncryption(xmlStr string) (encStr *string) {
	encStrtemp := base64.StdEncoding.EncodeToString([]byte(xmlStr))
	return &encStrtemp
}

func main() {
	// 调用flag函数输出命令行参数提示
	phonestr, alarmstr := flagInfo()
	if len(phonestr) == 0 {
		fmt.Println("Error: The Phone Number is Null")
		return
	}
	for _, value := range strings.Split(phonestr, ",") {
		v := newXml(value, alarmstr)
		// 调用MarshalIndent()函数构建ReqXml文件
		ReqXml, err := xml.MarshalIndent(v, "", " ")
		if err != nil {
			panic(err)
		}
		// 添加xml请求头
		ReqXml = append([]byte(xmlHeader), ReqXml...)
		fmt.Printf("Messagebuf: [%s] \n", string(ReqXml))

		// 对xml文件进行加密
		ReqEnc := xmlTEncryption(string(ReqXml))
		tmp := sendMq(ReqEnc)
		fmt.Printf("Base64buf: [%s] \n", *ReqEnc)

		// 调用SmsSendMQ接口
		SmsSendMQ("POST", tmp)
	}
}
