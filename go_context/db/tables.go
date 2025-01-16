package db

import (
	"fmt"

	"database/sql"

	_ "github.com/lib/pq"
)

func CreateTables(conn *sql.DB) error {
	if err := CreateLongOperationPointTable(conn); err != nil {
		return fmt.Errorf("failed to create long operation point table: %w", err)
	}

	if err := CreateShortOperationPointTable(conn); err != nil {
		return fmt.Errorf("failed to create short operation point table: %w", err)
	}

	if err := CreateIndicatorTable(conn); err != nil {
		return fmt.Errorf("failed to create indicator table: %w", err)
	}

	if err := CreateStrategyTable(conn); err != nil {
		return fmt.Errorf("failed to create strategy table: %w", err)
	}

	return nil
}

func CreateLongOperationPointTable(conn *sql.DB) error {
	CreateLongOperationPointTableStatement := `
	CREATE TABLE IF NOT EXISTS long_operation_point (
		id SERIAL PRIMARY KEY,
		instrument TEXT NOT NULL,
		datetime TIMESTAMP NOT NULL,
		result INT NOT NULL,
		tp INT NOT NULL,
		sl INT NOT NULL,
		long_balance INT[] NOT NULL,
		money_management_strategy_id INT NOT NULL
	);`

	_, err := conn.Exec(CreateLongOperationPointTableStatement)
	if err != nil {
		return err
	}
	return nil
}

func CreateShortOperationPointTable(conn *sql.DB) error {
	CreateShortOperationPointTableStatement := `
	CREATE TABLE IF NOT EXISTS short_operation_point (
		id SERIAL PRIMARY KEY,
		instrument TEXT NOT NULL,
		datetime TIMESTAMP NOT NULL,
		result INT NOT NULL,
		tp INT NOT NULL,
		sl INT NOT NULL,
		short_balance INT[] NOT NULL,
		money_management_strategy_id INT NOT NULL
	);`

	_, err := conn.Exec(CreateShortOperationPointTableStatement)
	if err != nil {
		return err
	}
	return nil
}

func CreateIndicatorTable(conn *sql.DB) error {
	CreateIndicatorTableStatement := `
	CREATE TABLE IF NOT EXISTS indicator (
		id SERIAL PRIMARY KEY,
		type VARCHAR NOT NULL,
		parameters JSON NOT NULL,
		identifier VARCHAR NOT NULL
	);`

	_, err := conn.Exec(CreateIndicatorTableStatement)
	if err != nil {
		return err
	}
	return nil
}

func CreateStrategyTable(conn *sql.DB) error {
	CreateStrategyTableStatement := `
	CREATE TABLE IF NOT EXISTS strategy (
		id SERIAL PRIMARY KEY,
		annual_roi FLOAT NOT NULL,
		max_draw_down FLOAT NOT NULL,
		min_annual_roi FLOAT NOT NULL,
		annual_operation_count FLOAT NOT NULL,
		money_management_strategy_id INTEGER NOT NULL,
		indicator_id INTEGER NOT NULL
	);`

	_, err := conn.Exec(CreateStrategyTableStatement)
	if err != nil {
		return err
	}
	return nil
}
