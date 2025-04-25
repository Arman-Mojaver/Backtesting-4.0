package ps

import (
	"math"
	"sort"
	"time"
)

func process(processData ProcessData) StrategyItem {
	longOperationPoints, longOperationPointIDs := getPointsAndIDs(processData.Signals.LongSignals, processData.LongOperationPoints)
	shortOperationPoints, shortOperationPointIDs := getPointsAndIDs(processData.Signals.ShortSignals, processData.ShortOperationPoints)

	operationPoints := append(longOperationPoints, shortOperationPoints...)
	sortOperationPoints(operationPoints)

	annualOperationCount := getAnnualOperationCount(processData.StartDate, processData.EndDate, len(operationPoints))
	maxDrawDown := calculateMaxDrawDown(operationPoints)

	strategy := StrategyData{
		AnnualROI:                 0.0,
		MaxDrawDown:               maxDrawDown,
		AnnualOperationCount:      annualOperationCount,
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
		dateFormat := "2006-01-02"
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

func getAnnualOperationCount(startDate string, endDate string, operationPointsCount int) float64 {
	differenceInYears := getDifferenceInYears(startDate, endDate)
	if differenceInYears == 0 {
		return 0.0
	}
	return float64(operationPointsCount) / differenceInYears
}

func stringToDatetime(dateStr string) (time.Time, error) {
	layout := "2006-01-02" // Define the expected date format
	return time.Parse(layout, dateStr)
}

func round(value float64, places int) float64 {
	scale := float64(math.Pow(10, float64(places)))
	return float64(math.Round(float64(value)*float64(scale)) / float64(scale))
}

func getMax(values []float64) float64 {
	if len(values) == 0 {
		return 0
	}

	maxVal := values[0]
	for _, v := range values {
		if v > maxVal {
			maxVal = v
		}
	}
	return maxVal
}

func calculateMaxDrawDown(operationPoints []OperationPoint) float64 {
	cumsum := 1.0
	cummax := 1.0
	draw_downs := []float64{}

	for _, operationPoint := range operationPoints {
		result := float64(operationPoint.Result) * operationPoint.Risk / float64(operationPoint.Sl)
		cumsum += result
		cummax = max(cummax, cumsum)
		draw_down := (cummax - cumsum) / cummax
		rounded_draw_down := round(draw_down*100, 2)
		draw_downs = append(draw_downs, rounded_draw_down)
	}

	return getMax(draw_downs)
}
