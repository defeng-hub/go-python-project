package initialize

import (
	"go.uber.org/zap"
)

// debug info warn

func NewLogger() (*zap.Logger, error) {
	cfg := zap.NewProductionConfig()
	cfg.OutputPaths = []string{
		".logs/user_web.logs",
	}
	return cfg.Build()
}

func InitZapLogger() {
	logger, err := zap.NewDevelopment()
	if err != nil {
		panic(err.Error())
	}
	zap.ReplaceGlobals(logger)
	// 全局 zap.S() 就是sugar
	// 全局 zap.L() 就是logger
	zap.S().Infow("logger初始化成功")
	return
}
