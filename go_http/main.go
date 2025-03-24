package main

import (
	"encoding/json"
	"io"
	"log"
	"math"
	"net/http"
	"os"
	"sort"
	"time"
)

func main() {
	// Setup logging
	file, err := os.OpenFile("logs/go-http.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("Failed to open log file: %s", err)
	}
	defer file.Close()

	multiWriter := io.MultiWriter(os.Stdout, file)
	log.SetOutput(multiWriter)
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	// Setup server
	mux := http.NewServeMux()
	mux.HandleFunc("/", indexHandler)
	mux.HandleFunc("/ping", pingHandler)
	mux.HandleFunc("/process_strategies", processStrategiesHandler)

	log.Println("Server starting on port 80...")
	log.Fatal(http.ListenAndServe(":80", mux))
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"message": "Server Working. Endpoint not defined!"}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"message": "Ping!"}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	log.Println("GET /ping")
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

func processStrategiesHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		response := map[string]string{"error": "Method Not Allowed"}
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(response)
		return
	}

	var payload RequestPayload
	decoder := json.NewDecoder(r.Body)
	defer r.Body.Close()

	if err := decoder.Decode(&payload); err != nil {
		response := map[string]string{"error": "Invalid JSON"}
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(response)
		return
	}

	var strategyItems []StrategyItem
	for moneyManagementStrategyID, operationPoints := range payload.OperationPoints {
		for indicatorID, signals := range payload.Signals {
			longOperationPoints := []OperationPoint{}
			longOperationPointIDs := []int{}
			for _, signal := range signals.LongSignals {
				longOperationPoint := operationPoints.LongOperationPoints[signal]
				longOperationPoints = append(longOperationPoints, longOperationPoint)
				longOperationPointIDs = append(longOperationPointIDs, longOperationPoint.ID)
			}

			shortOperationPoints := []OperationPoint{}
			shortOperationPointIDs := []int{}
			for _, signal := range signals.ShortSignals {
				shortOperationPoint := operationPoints.ShortOperationPoints[signal]
				shortOperationPoints = append(shortOperationPoints, shortOperationPoint)
				shortOperationPointIDs = append(shortOperationPointIDs, shortOperationPoint.ID)
			}

			operationPoints := append(longOperationPoints, shortOperationPoints...)
			sort.Slice(operationPoints, func(i, j int) bool {
				dateFormat := "2001-01-13"

				ti, _ := time.Parse(dateFormat, operationPoints[i].Datetime)
				tj, _ := time.Parse(dateFormat, operationPoints[j].Datetime)
				return ti.Before(tj)
			})
			differenceInYears := getDifferenceInYears(payload.StartDate, payload.EndDate)

			strategy := StrategyData{
				AnnualROI:            0.0,
				MaxDrawDown:          0.0,
				AnnualOperationCount: float64(len(operationPoints)) / differenceInYears,
				MoneyManagementStrategyID: moneyManagementStrategyID,
				IndicatorID: indicatorID,
			}
			strategyResponse := StrategyItem{
				StrategyData:           strategy,
				LongOperationPointIds:  longOperationPointIDs,
				ShortOperationPointIds: shortOperationPointIDs,
			}

			strategyItems = append(strategyItems, strategyResponse)
		}
	}

	response := Response{Data: strategyItems}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	log.Printf("POST /process_strategies")
}
