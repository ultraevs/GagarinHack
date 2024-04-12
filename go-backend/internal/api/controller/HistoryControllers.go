package controller

import (
	"app/internal/database"
	"app/internal/model"
	"database/sql"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
)

// GetHistory godoc
// @Summary Get User History
// @Description Return User's detection history
// @Produce json
// @Tags History
// @Success 200 {object} model.CodeResponse
// @Router /v1/gethistorylist [get]
func GetHistory(context *gin.Context) {
	tokenInterface, exists := context.Get("token")
	if !exists {
		context.JSON(http.StatusBadRequest, gin.H{"error": "token cookie not found"})
		return
	}

	token, ok := tokenInterface.(string)
	if !ok {
		context.JSON(http.StatusBadRequest, gin.H{"error": "invalid token type"})
		return
	}

	rows, err := database.Db.Query("SELECT date, count, recognize FROM gagarin_history WHERE token = $1", token)
	if err != nil {
		fmt.Println(err)
		context.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get get user's history"})
		return
	}
	defer func(rows *sql.Rows) {
		err := rows.Close()
		if err != nil {

		}
	}(rows)
	var histories []model.History
	for rows.Next() {
		var history model.History
		if err := rows.Scan(&history.Date, &history.Count, &history.Recognize); err != nil {
			fmt.Println(err)
			context.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to scan user's history"})
			return
		}
		histories = append(histories, history)
	}
	context.JSON(http.StatusOK, gin.H{"response": histories})
}

// PutHistory godoc
// @Summary Update User History
// @Description Put new item in User's history
// @Produce json
// @Param request body model.History true "Запрос на создание новой записи в истории пользователя"
// @Tags History
// @Success 200 {object} model.CodeResponse
// @Router /v1/puthistorylist [post]
func PutHistory(context *gin.Context) {
	tokenInterface, exists := context.Get("token")
	if !exists {
		context.JSON(http.StatusBadRequest, gin.H{"error": "token cookie not found"})
		return
	}

	token, ok := tokenInterface.(string)
	if !ok {
		context.JSON(http.StatusBadRequest, gin.H{"error": "invalid token type"})
		return
	}

	var request model.History
	if err := context.ShouldBindJSON(&request); err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"error": "Can't read the body"})
		return
	}
	_, err := database.Db.Exec("INSERT INTO gagarin_history (token, date, count, recognize) VALUES ($1, $2, $3, $4)", token, request.Date, request.Count, request.Recognize)
	if err != nil {
		fmt.Println(err)
		context.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to put item for user's history "})
		return
	}
	context.JSON(http.StatusOK, gin.H{"response": "success"})
}
