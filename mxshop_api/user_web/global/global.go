package global

import (
	ut "github.com/go-playground/universal-translator"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"user_web/config"
)

var (
	VIPER  *viper.Viper
	LOG    *zap.Logger
	CONFIG *config.Config
	Trans  ut.Translator
)
