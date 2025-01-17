package db

import (
	"fmt"

	"database/sql"
)

func DeleteEntries(conn *sql.DB) error {
	if err := DeleteTableEntries(conn, "resampled_point_d1"); err != nil {
		return fmt.Errorf("failed to delete resampled_point_d1 table entries: %w", err)
	}

	if err := DeleteTableEntries(conn, "long_operation_point"); err != nil {
		return fmt.Errorf("failed to delete long_operation_point table entries: %w", err)
	}

	if err := DeleteTableEntries(conn, "short_operation_point"); err != nil {
		return fmt.Errorf("failed to delete short_operation_point table entries: %w", err)
	}

	if err := DeleteTableEntries(conn, "indicator"); err != nil {
		return fmt.Errorf("failed to delete indicator table entries: %w", err)
	}

	if err := DeleteTableEntries(conn, "strategy"); err != nil {
		return fmt.Errorf("failed to delete strategy table entries: %w", err)
	}

	return nil
}

func DeleteTableEntries(conn *sql.DB, tableName string) error {
	query := fmt.Sprintf("DELETE FROM %s", tableName)

	_, err := conn.Exec(query)
	if err != nil {
		return fmt.Errorf("failed to delete records from table %s: %w", tableName, err)
	}

	return nil
}
