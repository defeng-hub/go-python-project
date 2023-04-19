package middleware

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"user_web/utils"
)

func IsAdmin() gin.HandlerFunc {
	return func(c *gin.Context) {
		clamis, err := utils.GetClaims(c)
		if clamis.AuthorityId != 2 || err != nil {
			c.JSON(http.StatusForbidden, gin.H{"msg": "无权限"})
			c.Abort()
			return
		}
		c.Next()
	}
}
