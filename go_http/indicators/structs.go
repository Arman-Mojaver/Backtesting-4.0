package in

// Request Structs

type RequestPayload struct {
	Instrument      string           `json:"instrument"`
	ResampledPoints []ResampledPoint `json:"resampled_points"`
	Indicators      []Indicator      `json:"indicators"`
}

type ResampledPoint struct {
	ID           int     `json:"id"`
	Datetime     string  `json:"datetime"`
	Instrument   string  `json:"instrument"`
	Open         float64 `json:"open"`
	High         float64 `json:"high"`
	Low          float64 `json:"low"`
	Close        float64 `json:"close"`
	Volume       int     `json:"volume"`
	HighLowOrder string  `json:"high_low_order"`
}

type Indicator struct {
	ID         int         `json:"id"`
	Type       string      `json:"type"`
	Parameters interface{} `json:"parameters"`
	Identifier string      `json:"identifier"`
}

type Response struct {
	Data int `json:"data"`
}
