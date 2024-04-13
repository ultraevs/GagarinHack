package router

import (
	"app/internal/api/controller"
	"app/internal/api/middleware"
	"github.com/gin-gonic/gin"
)

func (router *Router) HistoryRouters(group *gin.RouterGroup) {
	group.GET("/gethistorylist", middleware.CookieMiddleware(), controller.GetHistory)
	group.POST("/puthistorylist", middleware.CookieMiddleware(), controller.PutHistory)
}
