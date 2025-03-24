package main

import (
	"math"
	"sort"
	"time"
)

// Request Structs

type OperationPoint struct {
	ID                        int     `json:"id"`
	Instrument                string  `json:"instrument"`
	Datetime                  string  `json:"datetime"`
	Result                    int     `json:"result"`
	Tp                        int     `json:"tp"`
	Sl                        int     `json:"sl"`
	Risk                      float64 `json:"risk"`
	MoneyManagementStrategyID int     `json:"money_management_strategy_id"`
}

type OperationPoints struct {
	LongOperationPoints  map[string]OperationPoint `json:"long_operation_points"`
	ShortOperationPoints map[string]OperationPoint `json:"short_operation_points"`
}

type Signals struct {
	LongSignals  []string `json:"long_signals"`
	ShortSignals []string `json:"short_signals"`
}

type RequestPayload struct {
	OperationPoints map[int]OperationPoints `json:"operation_points"`
	Signals         map[int]Signals         `json:"signals"`
	StartDate       string                  `json:"start_date"`
	EndDate         string                  `json:"end_date"`
}

// Response Structs
type StrategyData struct {
	AnnualROI                 float64 `json:"annual_roi"`
	MaxDrawDown               float64 `json:"max_draw_down"`
	AnnualOperationCount      float64 `json:"annual_operation_count"`
	MoneyManagementStrategyID int     `json:"money_management_strategy_id"`
	IndicatorID               int     `json:"indicator_id"`
}

type StrategyItem struct {
	StrategyData           StrategyData `json:"strategy_data"`
	LongOperationPointIds  []int        `json:"long_operation_point_ids"`
	ShortOperationPointIds []int        `json:"short_operation_point_ids"`
}

type Response struct {
	Data []StrategyItem `json:"data"`
}

func stringToDatetime(dateStr string) (time.Time, error) {
	layout := "2006-01-02" // Define the expected date format
	return time.Parse(layout, dateStr)
}

func getDifferenceInYears(date1, date2 string) float64 {
	const daysInYear = 365.25

	parsedDate1, err := stringToDatetime(date1)
	if err != nil {
		panic(err)
	}
	parsedDate2, err := stringToDatetime(date2)
	if err != nil {
		panic(err)
	}

	duration := parsedDate1.Sub(parsedDate2).Hours() / 24
	return math.Round(math.Abs(duration)/daysInYear*100) / 100
}

func getPointsAndIDs(signals []string, operationPointsMap map[string]OperationPoint) ([]OperationPoint, []int) {
	var operationPoints []OperationPoint
	var operationPointIDs []int
	for _, signal := range signals {
		operationPoint := operationPointsMap[signal]
		operationPoints = append(operationPoints, operationPoint)
		operationPointIDs = append(operationPointIDs, operationPoint.ID)
	}
	return operationPoints, operationPointIDs
}

func sortOperationPoints(operationPoints []OperationPoint) {
	sort.Slice(operationPoints, func(i, j int) bool {
		dateFormat := "2001-01-13"
		ti, _ := time.Parse(dateFormat, operationPoints[i].Datetime)
		tj, _ := time.Parse(dateFormat, operationPoints[j].Datetime)
		return ti.Before(tj)
	})
}

func ProcessStrategies(payload RequestPayload) []StrategyItem {
	var strategyItems []StrategyItem
	for moneyManagementStrategyID, operationPoints := range payload.OperationPoints {
		for indicatorID, signals := range payload.Signals {
			longOperationPoints, longOperationPointIDs := getPointsAndIDs(signals.LongSignals, operationPoints.LongOperationPoints)
			shortOperationPoints, shortOperationPointIDs := getPointsAndIDs(signals.ShortSignals, operationPoints.ShortOperationPoints)

			operationPoints := append(longOperationPoints, shortOperationPoints...)
			sortOperationPoints(operationPoints)
			differenceInYears := getDifferenceInYears(payload.StartDate, payload.EndDate)

			strategy := StrategyData{
				AnnualROI:                 0.0,
				MaxDrawDown:               0.0,
				AnnualOperationCount:      float64(len(operationPoints)) / differenceInYears,
				MoneyManagementStrategyID: moneyManagementStrategyID,
				IndicatorID:               indicatorID,
			}
			strategyResponse := StrategyItem{
				StrategyData:           strategy,
				LongOperationPointIds:  longOperationPointIDs,
				ShortOperationPointIds: shortOperationPointIDs,
			}

			strategyItems = append(strategyItems, strategyResponse)
		}
	}

	return strategyItems
}
