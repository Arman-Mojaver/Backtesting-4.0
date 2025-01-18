package db

import (
	"database/sql"
	"errors"
	"fmt"
	"time"

	"github.com/lib/pq"
)

var ErrorNoLongOperationPoints = errors.New("no entries in long_operation_point table")
var ErrorNoShortOperationPoints = errors.New("no entries in short_operation_point table")

func convertInt64ToInt(input []int64) []int {
	result := make([]int, len(input))
	for i, v := range input {
		result[i] = int(v)
	}
	return result
}

func convertTimestamp(timestamp string) string {
	parsedTime, err := time.Parse(time.RFC3339, timestamp)
	if err != nil {
		return ""
	}

	return parsedTime.Format("2006-01-02") // Just used for specifying the format not actual value
}

func queryLongOperationPoints(conn *sql.DB) ([]LongOperationPoint, error) {
	query := `
		SELECT id, instrument, datetime, result, tp, sl, long_balance, risk, money_management_strategy_id
		FROM long_operation_point
	`

	rows, err := conn.Query(query)
	if err != nil {
		return nil, fmt.Errorf("error querying long_operation_point: %w", err)
	}
	defer rows.Close()

	var points []LongOperationPoint

	for rows.Next() {
		var point LongOperationPoint
		var longBalance []int64
		var datetime string

		err := rows.Scan(
			&point.ID,
			&point.Instrument,
			&datetime,
			&point.Result,
			&point.Tp,
			&point.Sl,
			pq.Array(&longBalance),
			&point.Risk,
			&point.MoneyManagementStrategyID,
		)
		if err != nil {
			return nil, fmt.Errorf("error scanning row: %w", err)
		}

		point.LongBalance = convertInt64ToInt(longBalance)
		point.Datetime = convertTimestamp(datetime)

		points = append(points, point)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("rows iteration error: %w", err)
	}

	return points, nil
}


func queryShortOperationPoints(conn *sql.DB) ([]ShortOperationPoint, error) {
	query := `
		SELECT id, instrument, datetime, result, tp, sl, short_balance, risk, money_management_strategy_id
		FROM short_operation_point
	`

	rows, err := conn.Query(query)
	if err != nil {
		return nil, fmt.Errorf("error querying short_operation_point: %w", err)
	}
	defer rows.Close()

	var points []ShortOperationPoint

	for rows.Next() {
		var point ShortOperationPoint
		var shortBalance []int64
		var datetime string

		err := rows.Scan(
			&point.ID,
			&point.Instrument,
			&datetime,
			&point.Result,
			&point.Tp,
			&point.Sl,
			pq.Array(&shortBalance),
			&point.Risk,
			&point.MoneyManagementStrategyID,
		)
		if err != nil {
			return nil, fmt.Errorf("error scanning row: %w", err)
		}

		point.ShortBalance = convertInt64ToInt(shortBalance)
		point.Datetime = convertTimestamp(datetime)

		points = append(points, point)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("rows iteration error: %w", err)
	}

	return points, nil
}



func GetLongOperationPoints(conn *sql.DB) ([]LongOperationPoint, error) {
	longOperationPoints, err := queryLongOperationPoints(conn)
	if err != nil {
		return []LongOperationPoint{}, err
	}

	if len(longOperationPoints) == 0 {
		return []LongOperationPoint{}, ErrorNoLongOperationPoints
	}

	return longOperationPoints, nil
}


func GetShortOperationPoints(conn *sql.DB) ([]ShortOperationPoint, error) {
	shortOperationPoints, err := queryShortOperationPoints(conn)
	if err != nil {
		return []ShortOperationPoint{}, err
	}

	if len(shortOperationPoints) == 0 {
		return []ShortOperationPoint{}, ErrorNoShortOperationPoints
	}

	return shortOperationPoints, nil
}
