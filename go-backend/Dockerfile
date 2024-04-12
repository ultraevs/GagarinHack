FROM golang:1.21.0-bookworm
WORKDIR /app

COPY go.mod ./
COPY go.sum ./

RUN go mod download

COPY cmd/ ./cmd/
COPY internal/ ./internal/
COPY templates/ ./templates/
COPY .env .

RUN go install github.com/swaggo/swag/cmd/swag@latest
RUN swag init -g /cmd/app/main.go
RUN go build -o ./main ./cmd/app/main.go

CMD [ "./main" ]
