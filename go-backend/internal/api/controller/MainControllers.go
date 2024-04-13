package controller

import (
	"github.com/gin-gonic/gin"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
)

// PutFile godoc
// @Summary Put Files From User
// @Description Put files from user to recognize
// @Produce json
// @Accept multipart/form-data
// @Param files formData []file true "Files to upload" collectionFormat(multi)
// @Tags Files
// @Success 200 {object} model.CodeResponse
// @Router /v1/putfile [post]
func PutFile(context *gin.Context) {
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

	form, err := context.MultipartForm()
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	files := form.File["files"]
	for _, file := range files {
		err := saveUploadedFile(file, token)
		if err != nil {
			context.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
	}

	context.JSON(http.StatusOK, gin.H{"response": "success"})
}

func saveUploadedFile(file *multipart.FileHeader, userID string) error {
	src, err := file.Open()
	if err != nil {
		return err
	}
	defer func(src multipart.File) {
		err := src.Close()
		if err != nil {

		}
	}(src)

	userDir := filepath.Join("./uploads", userID)
	err = os.MkdirAll(userDir, os.ModePerm)
	if err != nil {
		return err
	}

	dstPath := filepath.Join(userDir, file.Filename)
	dst, err := os.Create(dstPath)
	if err != nil {
		return err
	}
	defer func(dst *os.File) {
		err := dst.Close()
		if err != nil {

		}
	}(dst)

	_, err = io.Copy(dst, src)
	if err != nil {
		return err
	}

	return nil
}

func Main(context *gin.Context) {
	context.HTML(http.StatusOK, "index.html", gin.H{"response": "success"})
}
