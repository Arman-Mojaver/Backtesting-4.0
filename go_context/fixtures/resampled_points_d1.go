package fixtures

import "strategy/db"

var ResampledPointsD1 = []db.ResampledPointD1{
	{
		Datetime:     "2025-01-15",
		Instrument:   "EURUSD",
		Open:         1.2345,
		High:         1.2400,
		Low:          1.2300,
		Close:        1.2350,
		Volume:       1500,
		HighLowOrder: "high_first",
	},
	{
		Datetime:     "2025-01-16",
		Instrument:   "EURUSD",
		Open:         1.2345,
		High:         1.2400,
		Low:          1.2300,
		Close:        1.2350,
		Volume:       2000,
		HighLowOrder: "low_first",
	},
}
