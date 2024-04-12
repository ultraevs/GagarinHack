package router

import (
	"app/internal/api/controller"
	"app/internal/api/middleware"
	"github.com/gin-gonic/gin"
)

func (router *Router) MainRoutes(group *gin.RouterGroup) {
	group.POST("/putfile", middleware.CookieMiddleware(), controller.PutFile)
	router.engine.GET("/", controller.Main)
}
