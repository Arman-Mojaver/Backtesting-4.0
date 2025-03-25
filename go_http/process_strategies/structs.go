package ps

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

// Channel structs

type ProcessData struct {
	Instrument                string
	MoneyManagementStrategyID int
	IndicatorID               int
	OperationPoints           OperationPoints
	Signals                   Signals
	StartDate                 string
	EndDate                   string
}
