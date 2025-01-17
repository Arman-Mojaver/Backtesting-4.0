package fixtures

import "strategy/db"

var ShortOperationPoints = []db.ShortOperationPoint{
	{
		Instrument:                "EURUSD",
		Datetime:                  "2025-01-15",
		Result:                    -120,
		Tp:                        80,
		Sl:                        120,
		ShortBalance:              []int{800, 700, 600},
		Risk:                      0.03,
		MoneyManagementStrategyID: 1,
	},
	{
		Instrument:                "EURUSD",
		Datetime:                  "2025-01-16",
		Result:                    250,
		Tp:                        250,
		Sl:                        150,
		ShortBalance:              []int{2000, 2500, 3000},
		Risk:                      0.02,
		MoneyManagementStrategyID: 1,
	},
}
