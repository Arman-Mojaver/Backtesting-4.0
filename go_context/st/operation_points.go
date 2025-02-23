package st

import (
	"database/sql"
	"errors"
	"fmt"
	"strategy/db"
	"sort"
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

func GetOperationPointsMap(operationPoints OperationPoints) (int, error) {
	if !operationPointsMatch(operationPoints) {
		return 0, ErrOperationPointsMismatch
	}

	return 0, nil

}
