package middleware

import (
	"net/http"
	"user_web/utils"

	"github.com/gin-gonic/gin"
)

func JWTAuth() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 我们这里jwt鉴权取头部信息 x-token 登录时回返回token信息
		// 这里前端需要把token存储到cookie或者本地localStorage中
		// 不过需要跟后端协商过期时间 可以约定刷新令牌或者重新登录
		token := c.Request.Header.Get("x-token")
		if token == "" {
			c.JSON(http.StatusOK, gin.H{
				"msg": "未登录或非法访问",
			})
			c.Abort()
			return
		}

		j := utils.NewJWT()
		// parseToken 解析token包含的信息
		claims, err := j.ParseToken(token)
		if err != nil {
			if err == utils.TokenExpired {
				c.JSON(http.StatusOK, gin.H{"msg": "授权已过期"})
				c.Abort()
				return
			}
			c.JSON(http.StatusOK, gin.H{"msg": err.Error()})
			c.Abort()
			return
		}
		c.Set("claims", claims)
		c.Next()
	}
}
