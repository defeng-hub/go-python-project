package main

import (
	"user_web/initialize"
)

func main() {
	initialize.InitZapLogger()
	Router := initialize.InitRouter()

	if err := Router.Run(":8021"); err != nil {
		panic("打开服务器失败")
		return
	}
}
