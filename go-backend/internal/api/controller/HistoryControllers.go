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
// @Summary Get History
// @Description Return  detection history
// @Produce json
// @Tags History
// @Success 200 {object} model.CodeResponse
// @Router /v1/gethistorylist [get]
func GetHistory(context *gin.Context) {
	rows, err := database.Db.Query("SELECT id, date, type, status FROM gagarin_history")
	if err != nil {
		fmt.Println(err)
		context.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get get history"})
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
			context.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to scan history"})
			return
		}
		histories = append(histories, history)
	}
	context.JSON(http.StatusOK, gin.H{"response": histories})
}
