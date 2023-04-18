package initialize

import (
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	router "user_web/router"
)

func InitRouter() *gin.Engine {
	//gin.SetMode(gin.ReleaseMode)
	engine := gin.Default()
	apiGroup := engine.Group("/u/v1")

	router.InitUserRouter(apiGroup)
	zap.S().Infow("gin初始化成功")

	return engine
}
