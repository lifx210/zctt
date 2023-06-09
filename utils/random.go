package utils

import (
	"fmt"
	"math/rand"
	"strings"
	"time"
)

func Random(min, max int) int {
	/*
		min,max: 生成随机数的取值范围
	*/
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(max-min+1) + min
}

func RandomUser(userMinLen, userMaxLen, num int, UppName bool) []string {
	/*
		userMinLen: 用户名字符串最小长度
		userMaxLen: 用户名字符串最大长度
			   num: 生成用户名个数
		   UppName: 用户名首字母是否大写，ture--大写，false--小写
	*/
	var userList = make([]string, num)

	for x := 0; x < num; x++ {
		var user string = ""
		userLen := Random(userMinLen, userMaxLen)

		for y := 0; y < userLen; y++ {
			userNum := Random(97, 122)
			user += fmt.Sprintf("%c", userNum)
		}
		if UppName {
			userList = append(userList, strings.ToTitle((user))[1:])
		} else {
			userList = append(userList, user)[1:]
		}

	}
	return userList
}

func RandomPwd(pwdLen, num int) []string {
	/*
		pwdLen: 密码长度
		   num: 生成的密码个数
	*/
	var pwdList = make([]string, num)

	for x := 0; x < num; x++ {
		var pwd string = ""
		pwdLen := Random(pwdLen, pwdLen)

		for y := 0; y < pwdLen; y++ {
			pwdNum := Random(33, 126)
			if pwdNum == 92 {
				continue
			}
			pwd += fmt.Sprintf("%c", pwdNum)
		}
		pwdList = append(pwdList, pwd)[1:]
	}
	return pwdList
}
