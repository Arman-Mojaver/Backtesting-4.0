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

func InsertLongOperationPoints(conn *sql.DB, points []LongOperationPoint) ([]LongOperationPoint, error) {
	InsertStatement := `
	INSERT INTO long_operation_point (instrument, datetime, result, tp, sl, long_balance, risk, money_management_strategy_id)
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
			points[i].Instrument,
			points[i].Datetime,
			points[i].Result,
			points[i].Tp,
			points[i].Sl,
			points[i].LongBalance,
			points[i].Risk,
			points[i].MoneyManagementStrategyID,
		).Scan(&points[i].ID)
		if err != nil {
			transaction.Rollback()
			return nil, fmt.Errorf("failed to insert long operation point: %w", err)
		}
	}

	if err := transaction.Commit(); err != nil {
		return nil, fmt.Errorf("failed to commit transaction: %w", err)
	}

	return points, nil
}

func InsertShortOperationPoints(conn *sql.DB, points []ShortOperationPoint) ([]ShortOperationPoint, error) {
	InsertStatement := `
	INSERT INTO short_operation_point (instrument, datetime, result, tp, sl, short_balance, risk, money_management_strategy_id)
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
			points[i].Instrument,
			points[i].Datetime,
			points[i].Result,
			points[i].Tp,
			points[i].Sl,
			points[i].ShortBalance,
			points[i].Risk,
			points[i].MoneyManagementStrategyID,
		).Scan(&points[i].ID)
		if err != nil {
			transaction.Rollback()
			return nil, fmt.Errorf("failed to insert short operation point: %w", err)
		}
	}

	if err := transaction.Commit(); err != nil {
		return nil, fmt.Errorf("failed to commit transaction: %w", err)
	}

	return points, nil
}
