package db

import (
	"log"

	"fmt"

	_ "github.com/lib/pq"
)

func CreateDB(dbConfig DBConfig) error {
	conn, _ := ConnectDB(dbConfig.ConnStr())
	defer conn.Close()

	_, err := conn.Exec(fmt.Sprintf(`CREATE DATABASE "%s";`, dbConfig.DBName))
	if err != nil {
		log.Fatalf("Failed to create database: %v", err)
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
