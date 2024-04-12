package logging

import (
	"github.com/sirupsen/logrus"
	"io"
	"os"
)

var Log *logrus.Logger

func NewLogger() error {
	Log = logrus.New()
	logFile, err := os.OpenFile("backend.log", os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0644)
	if err != nil {
		return err
	}
	mw := io.MultiWriter(os.Stdout, logFile)
	Log.SetOutput(mw)
	Log.SetFormatter(&logrus.TextFormatter{
		FullTimestamp:   false,
		TimestampFormat: "2006-01-02 15:04:05",
	})
	logLevel := os.Getenv("LOG_LVL")
	switch logLevel {
	case "DEBUG":
		Log.SetLevel(logrus.DebugLevel)
	case "ERROR":
		Log.SetLevel(logrus.ErrorLevel)
	default:
		Log.SetLevel(logrus.InfoLevel)
	}
	return nil
}
