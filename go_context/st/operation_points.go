package st

import (
	"database/sql"
	"errors"
	"fmt"
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
