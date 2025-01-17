package fixtures

import "strategy/db"

var Indicators = []db.Indicator{
	{
		Type:       "macd",
		Parameters: `{"slow": {"type": "sma", "n": 12, "price_target": "close"},"fast": {"type": "ema", "n": 5, "price_target": "close"}}`,
		Identifier: "macd.sma-12-close,ema-5-close",
	},
	{
		Type:       "macd",
		Parameters: `{"slow": {"type": "sma", "n": 13, "price_target": "close"},"fast": {"type": "ema", "n": 2, "price_target": "close"}}`,
		Identifier: "macd.sma-13-close,ema-4-close",
	},
}
