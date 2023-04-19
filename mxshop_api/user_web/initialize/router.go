package initialize

import (
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	"go.uber.org/zap"
	"user_web/global"

	router "user_web/router"
	myvalidator "user_web/validator"
)

func InitRouter() *gin.Engine {
	//gin.SetMode(gin.ReleaseMode)
	engine := gin.Default()
	apiGroup := engine.Group("/u/v1")

	router.InitUserRouter(apiGroup)
	zap.S().Infow("gin初始化成功")
	return engine
}

func InitBinding() {
	//注册验证器
	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		_ = v.RegisterValidation("mobile", myvalidator.ValidateMobile)
		_ = v.RegisterTranslation("mobile", global.Trans, func(ut ut.Translator) error {
			return ut.Add("mobile", "{0} 非法的手机号码!", true)
		}, func(ut ut.Translator, fe validator.FieldError) string {
			t, _ := ut.T("mobile", fe.Field())
			return t
		})
	}
}
