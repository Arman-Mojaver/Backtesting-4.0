package db

import (
	"fmt"

	"database/sql"

	_ "github.com/lib/pq"
)

func InsertResampledPointsD1(conn *sql.DB, points []ResampledPointD1) ([]ResampledPointD1, error) {
	InsertStatement := `
	INSERT INTO resampled_point_d1 (datetime, instrument, open, high, low, close, volume, high_low_order)
	VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id;`

	transaction, err := conn.Begin()
	if err != nil {
		return nil, fmt.Errorf("failed to begin transaction: %w", err)
	}

	statement, err := transaction.Prepare(InsertStatement)
	if err != nil {
		transaction.Rollback()
		return nil, fmt.Errorf("failed to prepare statement: %w", err)
	}
	defer statement.Close()

	for i := range points {
		err := statement.QueryRow(
			points[i].Datetime,
			points[i].Instrument,
			points[i].Open,
			points[i].High,
			points[i].Low,
			points[i].Close,
			points[i].Volume,
			points[i].HighLowOrder,
		).Scan(&points[i].ID)
		if err != nil {
			transaction.Rollback()
			return nil, fmt.Errorf("failed to insert resampled point: %w", err)
		}
	}

	if err := transaction.Commit(); err != nil {
		return nil, fmt.Errorf("failed to commit transaction: %w", err)
	}

	return points, nil
}
