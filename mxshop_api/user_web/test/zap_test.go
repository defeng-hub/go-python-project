package test

import (
	"go.uber.org/zap"
	"testing"
	"time"
)

// zap 高性能日志的测试文件

// 测试初始化及 输出到控制台
func TestConsole(t *testing.T) {
	//logger, _ := zap.NewProduction() //生产环境
	logger, _ := zap.NewDevelopment() //开发环境
	defer logger.Sync()               // 刷新缓冲区（如果有）

	sugar := logger.Sugar()
	url := "www.baidu.com"
	sugar.Infow("failed to fetch URL",
		"url", url,
		"attempt", 3,
		"backoff", time.Second,
	)
	sugar.Infof("Failed to fetch URL: %s", url)
}

func NewLogger() (*zap.Logger, error) {
	cfg := zap.NewProductionConfig()
	cfg.OutputPaths = []string{
		"./myproject.logs",
		"stderr",
	}
	return cfg.Build()
}

func TestToFile(t *testing.T) {
	logger, err := NewLogger()
	if err != nil {
		panic(err)
		//panic("初始化logger失败")
	}
	su := logger.Sugar()
	defer su.Sync()
	url := "https://imooc.com"
	su.Info("failed to fetch URL",
		// Structured context as strongly typed Field values.
		zap.String("url", url),
		zap.Int("attempt", 3),
		zap.Duration("backoff", time.Second),
	)
}
