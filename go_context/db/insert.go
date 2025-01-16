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

func InsertIndicators(conn *sql.DB, indicators []Indicator) ([]Indicator, error) {
	InsertStatement := `
	INSERT INTO indicator (type, parameters, identifier)
	VALUES ($1, $2, $3) RETURNING id;`

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

	for i := range indicators {
		err := statement.QueryRow(
			indicators[i].Type,
			indicators[i].Parameters,
			indicators[i].Identifier,
		).Scan(&indicators[i].ID)
		if err != nil {
			transaction.Rollback()
			return nil, fmt.Errorf("failed to insert indicator: %w", err)
		}
	}

	if err := transaction.Commit(); err != nil {
		return nil, fmt.Errorf("failed to commit transaction: %w", err)
	}

	return indicators, nil
}

func InsertStrategies(conn *sql.DB, strategies []Strategy) ([]Strategy, error) {
	InsertStatement := `
	INSERT INTO strategy (annual_roi, max_draw_down, min_annual_roi, annual_operation_count, money_management_strategy_id, indicator_id)
	VALUES ($1, $2, $3, $4, $5, $6) RETURNING id;`

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

	for i := range strategies {
		err := statement.QueryRow(
			strategies[i].AnnualROI,
			strategies[i].MaxDrawDown,
			strategies[i].MinAnnualROI,
			strategies[i].AnnualOperationCount,
			strategies[i].MoneyManagementStrategyID,
			strategies[i].IndicatorID,
		).Scan(&strategies[i].ID)
		if err != nil {
			transaction.Rollback()
			return nil, fmt.Errorf("failed to insert strategy: %w", err)
		}
	}

	if err := transaction.Commit(); err != nil {
		return nil, fmt.Errorf("failed to commit transaction: %w", err)
	}

	return strategies, nil
}
