package fixtures

import "strategy/db"

var LongOperationPoints = []db.LongOperationPoint{
	{
		Instrument:                "EURUSD",
		Datetime:                  "2025-01-15",
		Result:                    120,
		Tp:                        120,
		Sl:                        80,
		LongBalance:               []int{1000, 1200, 1500},
		Risk:                      0.02,
		MoneyManagementStrategyID: 1,
	},
	{
		Instrument:                "EURUSD",
		Datetime:                  "2025-01-16",
		Result:                    -100,
		Tp:                        200,
		Sl:                        100,
		LongBalance:               []int{1500, 1800, 2000},
		Risk:                      0.01,
		MoneyManagementStrategyID: 1,
	},
}
