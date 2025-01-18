package db

import (
	"log"

	"fmt"

	_ "github.com/lib/pq"
)

func CreateDB(dbConfig DBConfig) error {
	conn, err := ConnectDB(dbConfig.ConnStr())
	if err != nil {
		return fmt.Errorf("failed to connect to database server: %w", err)
	}
	defer conn.Close()

	var exists bool
	query := `SELECT EXISTS (SELECT FROM pg_database WHERE datname = $1);`
	err = conn.QueryRow(query, dbConfig.DBName).Scan(&exists)
	if err != nil {
		return fmt.Errorf("failed to check if database exists: %w", err)
	}

	if !exists {
		_, err = conn.Exec(fmt.Sprintf(`CREATE DATABASE "%s";`, dbConfig.DBName))
		if err != nil {
			return fmt.Errorf("failed to create database: %w", err)
		}
	}

	return nil
}

func DropDB(dbConfig DBConfig) error {
	conn, _ := ConnectDB(dbConfig.ConnStr())
	defer conn.Close()

	_, err := conn.Exec(fmt.Sprintf(`DROP DATABASE IF EXISTS "%s";`, dbConfig.DBName))
	if err != nil {
		log.Fatalf("Failed to create database: %v", err)
	}
	return nil
}
