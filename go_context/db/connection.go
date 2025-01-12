package db

import (
	"database/sql"
	"fmt"

	_ "github.com/lib/pq"
)

func GetDBConfig(environment string) (DBConfig, error) {
	var config DBConfig

	switch environment {
	case "production":
		config = DBConfig{
			Host:     "db-production",
			Port:     5432,
			User:     "postgres",
			Password: "postgres",
			DBName:   "db-production",
			SSLMode:  "disable",
		}
	case "development":
		config = DBConfig{
			Host:     "db-development",
			Port:     54320,
			User:     "postgres",
			Password: "postgres",
			DBName:   "db-development",
			SSLMode:  "disable",
		}
	case "testing":
		config = DBConfig{
			Host:     "db-testing",
			Port:     54321,
			User:     "postgres",
			Password: "postgres",
			DBName:   "db-testing",
			SSLMode:  "disable",
		}

	default:
		return DBConfig{}, fmt.Errorf("unknown environment: %s", environment)
	}

	return config, nil
}

func ConnectDB(connStr string) (*sql.DB, error) {
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, err
	}

	err = db.Ping()
	if err != nil {
		return nil, err
	}

	return db, nil
}
