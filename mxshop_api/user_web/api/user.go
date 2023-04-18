package api

import (
	"context"
	"fmt"
	"net/http"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"

	"user_web/global"
	"user_web/global/forms"
	"user_web/global/response"
	"user_web/proto"
)

// 将grpc错误转化为 http错误码
func HandleGrpcErrorToHttp(err error, c *gin.Context) {
	//将grpc的code转换成http的状态码
	if err != nil {
		if e, ok := status.FromError(err); ok {
			switch e.Code() {
			case codes.NotFound:
				c.JSON(http.StatusNotFound, gin.H{
					"msg": e.Message(),
				})
			case codes.Internal:
				c.JSON(http.StatusInternalServerError, gin.H{
					"msg:": "内部错误",
				})
			case codes.InvalidArgument:
				c.JSON(http.StatusBadRequest, gin.H{
					"msg": "参数错误",
				})
			case codes.Unavailable:
				c.JSON(http.StatusInternalServerError, gin.H{
					"msg": "服务不可用",
				})
			default:
				c.JSON(http.StatusInternalServerError, gin.H{
					"msg": e.Code(),
				})
			}
			return
		}
	}
}

func removeTopStruct(fileds map[string]string) map[string]string {
	rsp := map[string]string{}
	for field, err := range fileds {
		rsp[field[strings.Index(field, ".")+1:]] = err
	}
	return rsp
}
func HandleValidatorError(c *gin.Context, err error) {
	errs, ok := err.(validator.ValidationErrors)
	if !ok {
		c.JSON(http.StatusOK, gin.H{
			"msg": err.Error(),
		})
	}
	c.JSON(http.StatusBadRequest, gin.H{
		"error": removeTopStruct(errs.Translate(global.Trans)),
	})
	return
}

func GetUserList(ctx *gin.Context) {
	// 连接grpc
	ip := "127.0.0.1"
	port := 50051
	dial, err := grpc.Dial(fmt.Sprintf("%s:%d", ip, port),
		grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		HandleGrpcErrorToHttp(err, ctx)
		return
	}

	tmp1, _ := strconv.Atoi(ctx.DefaultQuery("page", "0"))
	tmp2, _ := strconv.Atoi(ctx.DefaultQuery("pageSize", "5"))

	//生成grpc client
	userSrvClient := proto.NewUserClient(dial)

	rsp, err := userSrvClient.GetUserList(context.Background(), &proto.PageInfo{
		Page:     uint32(tmp1),
		PageSize: uint32(tmp2),
	})
	if err != nil {
		zap.S().Errorw("查询用户列表失败")
		HandleGrpcErrorToHttp(err, ctx)
		return
	}

	result := make([]interface{}, 0)
	for _, value := range rsp.Data {
		user := response.UserResponse{
			Id:       value.Id,
			Mobile:   value.Mobile,
			NickName: value.NickName,
			BirthDay: response.JsonTime(value.BirthDay),
			Gender:   value.Gender,
		}
		result = append(result, user)
	}
	ctx.JSON(http.StatusOK, result)
}

func GetUserById(ctx *gin.Context) {

}

func PasswordLogin(ctx *gin.Context) {
	form := forms.PasswordLoginForm{}
	if err := ctx.ShouldBind(&form); err != nil {
		HandleValidatorError(ctx, err)
		return
	}

}
