package config

type Config struct {
	Service Service `mapstructure:"Service"`
}

type Service struct {
	ServiceName string `mapstructure:"ServiceName"`
	IP          string `mapstructure:"IP"`
	Port        int    `mapstructure:"Port"`
}
