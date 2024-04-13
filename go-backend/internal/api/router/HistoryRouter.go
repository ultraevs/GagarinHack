package router

import (
	"app/internal/api/controller"
	"github.com/gin-gonic/gin"
)

func (router *Router) HistoryRouters(group *gin.RouterGroup) {
	group.GET("/gethistorylist", controller.GetHistory)
}
