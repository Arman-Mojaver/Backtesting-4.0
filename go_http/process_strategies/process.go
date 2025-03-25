package ps

import (
	"math"
	"sort"
	"time"
)

func process(processData ProcessData) StrategyItem {
	longOperationPoints, longOperationPointIDs := getPointsAndIDs(processData.Signals.LongSignals, processData.OperationPoints.LongOperationPoints)
	shortOperationPoints, shortOperationPointIDs := getPointsAndIDs(processData.Signals.ShortSignals, processData.OperationPoints.ShortOperationPoints)

	operationPoints := append(longOperationPoints, shortOperationPoints...)
	sortOperationPoints(operationPoints)
	differenceInYears := getDifferenceInYears(processData.StartDate, processData.EndDate)

	strategy := StrategyData{
		AnnualROI:                 0.0,
		MaxDrawDown:               0.0,
		AnnualOperationCount:      float64(len(operationPoints)) / differenceInYears,
		MoneyManagementStrategyID: processData.MoneyManagementStrategyID,
		IndicatorID:               processData.IndicatorID,
	}
	strategyItem := StrategyItem{
		StrategyData:           strategy,
		LongOperationPointIds:  longOperationPointIDs,
		ShortOperationPointIds: shortOperationPointIDs,
	}

	return strategyItem
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

func stringToDatetime(dateStr string) (time.Time, error) {
	layout := "2006-01-02" // Define the expected date format
	return time.Parse(layout, dateStr)
}
