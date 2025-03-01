package st

import (
	"database/sql"
	"errors"
	"fmt"
	"sort"
	"strategy/db"
)

var ErrGetLongOperationPoints = errors.New("query LongOperationPoints error")
var ErrGetShortOperationPoints = errors.New("query ShortOperationPoints error")

type OperationPoints struct {
	LongOperationPoints  []db.LongOperationPoint
	ShortOperationPoints []db.ShortOperationPoint
}

func GetOperationPoints(dbConn *sql.DB) (OperationPoints, error) {
	longOperationPoints, err := db.GetLongOperationPoints(dbConn)
	if err != nil {
		return OperationPoints{
			LongOperationPoints:  []db.LongOperationPoint{},
			ShortOperationPoints: []db.ShortOperationPoint{},
		}, errors.Join(fmt.Errorf("GetOperationPoints: %w", ErrGetLongOperationPoints), err)
	}
	shortOperationPoints, err := db.GetShortOperationPoints(dbConn)
	if err != nil {
		return OperationPoints{
			LongOperationPoints:  []db.LongOperationPoint{},
			ShortOperationPoints: []db.ShortOperationPoint{},
		}, errors.Join(fmt.Errorf("GetOperationPoints: %w", ErrGetShortOperationPoints), err)
	}

	return OperationPoints{
		LongOperationPoints:  longOperationPoints,
		ShortOperationPoints: shortOperationPoints,
	}, nil
}

// Instrument -> MoneyManagementStrategyID -> Datetime -> OperationPoint
type OperationPointsMaps struct {
	LongOperationPointsMap  map[string]map[int]map[string]db.LongOperationPoint
	ShortOperationPointsMap map[string]map[int]map[string]db.ShortOperationPoint
}

var ErrOperationPointsMismatch = errors.New("long and short Operation Points do not match")

func operationPointsMatch(operationPoints OperationPoints) bool {
	longDatesByInstrument := make(map[string][]string)
	shortDatesByInstrument := make(map[string][]string)

	for _, lop := range operationPoints.LongOperationPoints {
		longDatesByInstrument[lop.Instrument] = append(longDatesByInstrument[lop.Instrument], lop.Datetime)
	}

	for _, sop := range operationPoints.ShortOperationPoints {
		shortDatesByInstrument[sop.Instrument] = append(shortDatesByInstrument[sop.Instrument], sop.Datetime)
	}

	for instrument, longDates := range longDatesByInstrument {
		shortDates := shortDatesByInstrument[instrument]

		sort.Strings(longDates)
		sort.Strings(shortDates)

		if len(longDates) != len(shortDates) {
			return false
		}

		for i := range longDates {
			if longDates[i] != shortDates[i] {
				return false
			}
		}
	}

	return true
}

func createOperationPointsMap(operationPoints OperationPoints) OperationPointsMaps {
	operationPointsMap := OperationPointsMaps{
		LongOperationPointsMap:  make(map[string]map[int]map[string]db.LongOperationPoint),
		ShortOperationPointsMap: make(map[string]map[int]map[string]db.ShortOperationPoint),
	}

	// Long operation points map
	for _, point := range operationPoints.LongOperationPoints {
		if _, exists := operationPointsMap.LongOperationPointsMap[point.Instrument]; !exists {
			operationPointsMap.LongOperationPointsMap[point.Instrument] = make(map[int]map[string]db.LongOperationPoint)
		}

		if _, exists := operationPointsMap.LongOperationPointsMap[point.Instrument][point.MoneyManagementStrategyID]; !exists {
			operationPointsMap.LongOperationPointsMap[point.Instrument][point.MoneyManagementStrategyID] = make(map[string]db.LongOperationPoint)
		}

		operationPointsMap.LongOperationPointsMap[point.Instrument][point.MoneyManagementStrategyID][point.Datetime] = point
	}

	// Short operation points map
	for _, point := range operationPoints.ShortOperationPoints {
		if _, exists := operationPointsMap.ShortOperationPointsMap[point.Instrument]; !exists {
			operationPointsMap.ShortOperationPointsMap[point.Instrument] = make(map[int]map[string]db.ShortOperationPoint)
		}

		if _, exists := operationPointsMap.ShortOperationPointsMap[point.Instrument][point.MoneyManagementStrategyID]; !exists {
			operationPointsMap.ShortOperationPointsMap[point.Instrument][point.MoneyManagementStrategyID] = make(map[string]db.ShortOperationPoint)
		}

		operationPointsMap.ShortOperationPointsMap[point.Instrument][point.MoneyManagementStrategyID][point.Datetime] = point
	}

	return operationPointsMap
}

func GetOperationPointsMap(operationPoints OperationPoints) (OperationPointsMaps, error) {
	if !operationPointsMatch(operationPoints) {
		return OperationPointsMaps{}, ErrOperationPointsMismatch
	}

	operationPointsMap := createOperationPointsMap(operationPoints)

	return operationPointsMap, nil

}
