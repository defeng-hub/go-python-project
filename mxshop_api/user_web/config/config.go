package config

type Config struct {
	Service Service `mapstructure:"Service"`
	JWT     JWT     `mapstructure:"JWT"`
}

type Service struct {
	ServiceName string `mapstructure:"ServiceName"`
	IP          string `mapstructure:"IP"`
	Port        int    `mapstructure:"Port"`
}

type JWT struct {
	SigningKey string `mapstructure:"SigningKey"`
}
