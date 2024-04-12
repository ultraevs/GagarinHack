package model

type ErrorResponse struct {
	Error string `json:"error"`
}

type CodeResponse struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}
