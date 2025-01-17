package fixtures

import "strategy/db"

var Strategies = []db.Strategy{
	{
		AnnualROI:                 12.5,
		MaxDrawDown:               -5.0,
		MinAnnualROI:              10.0,
		AnnualOperationCount:      120,
		MoneyManagementStrategyID: 1,
		IndicatorID:               1,
	},
	{
		AnnualROI:                 15.0,
		MaxDrawDown:               -6.5,
		MinAnnualROI:              12.0,
		AnnualOperationCount:      140,
		MoneyManagementStrategyID: 2,
		IndicatorID:               2,
	},
}
