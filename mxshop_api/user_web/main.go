package main

import (
	"fmt"
	"user_web/global"
	"user_web/initialize"
)

func main() {
	initialize.InitZapLogger()
	initialize.Viper("./config/dev.yaml")
	Router := initialize.InitRouter()
	//4. 初始化翻译
	initialize.InitTrans("zh")

	if err := Router.Run(fmt.Sprintf("%s:%d",
		global.CONFIG.Service.IP, global.CONFIG.Service.Port)); err != nil {
		panic("打开服务器失败")
		return
	}
}
