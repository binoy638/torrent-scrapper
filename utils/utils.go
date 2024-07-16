package utils

import (
	"fmt"
	"log"
	"strconv"
	"strings"
	"time"
)

func TrimWhiteSpace(str string) string {
	return strings.TrimSpace(str)
}

func ParseSizeString(sizeStr string) (int64, error) {
	sizeStr = strings.ToLower(sizeStr)
	parts := strings.Fields(sizeStr)
	if len(parts) != 2 {
		return 0, fmt.Errorf("invalid size string format: %s", sizeStr)
	}

	size, err := strconv.ParseFloat(parts[0], 64)
	if err != nil {
		return 0, fmt.Errorf("failed to parse size: %v", err)
	}

	unit := parts[1]
	var multiplier int64

	switch unit {
	case "gb":
		multiplier = 1024 * 1024 * 1024
	case "mb":
		multiplier = 1024 * 1024
	case "kb":
		multiplier = 1024
	default:
		return 0, fmt.Errorf("unsupported size unit: %s", unit)
	}

	bytes := int64(size * float64(multiplier))
	return bytes, nil
}

func ParseInt(intStr string) int {
	intStr = strings.TrimSpace(intStr)
	intValue, err := strconv.Atoi(intStr)
	if err != nil {
		log.Printf("Unable to parse integer value: %s", intStr)
		return 0
	}
	return intValue
}

func FormatDate(dateStr string) (int64, error) {
	layout := "2006-01-02 15:04:05"
	dateTime, err := time.Parse(layout, dateStr)
	if err != nil {
		return 0, err
	}
	return dateTime.Unix(), nil
}
