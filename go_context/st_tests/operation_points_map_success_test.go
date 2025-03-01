package strategy_test

import (
	"github.com/stretchr/testify/require"
	"strategy/db"
	"strategy/st"
)

func (suite *TestSuite) TestGetOperationPointsMapOneInstrumentOneStrategy() {
	var longOperationPoints = []db.LongOperationPoint{
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

	var shortOperationPoints = []db.ShortOperationPoint{
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

	operationPoints := st.OperationPoints{
		LongOperationPoints:  longOperationPoints,
		ShortOperationPoints: shortOperationPoints,
	}
	operationPointsMap, err := st.GetOperationPointsMap(operationPoints)

	expectedResult := st.OperationPointsMaps{
		LongOperationPointsMap:  make(map[string]map[int]map[string]db.LongOperationPoint),
		ShortOperationPointsMap: make(map[string]map[int]map[string]db.ShortOperationPoint),
	}

	if _, ok := expectedResult.LongOperationPointsMap["EURUSD"]; !ok {
		expectedResult.LongOperationPointsMap["EURUSD"] = make(map[int]map[string]db.LongOperationPoint)
	}
	if _, ok := expectedResult.LongOperationPointsMap["EURUSD"][1]; !ok {
		expectedResult.LongOperationPointsMap["EURUSD"][1] = make(map[string]db.LongOperationPoint)
	}

	if _, ok := expectedResult.ShortOperationPointsMap["EURUSD"]; !ok {
		expectedResult.ShortOperationPointsMap["EURUSD"] = make(map[int]map[string]db.ShortOperationPoint)
	}
	if _, ok := expectedResult.ShortOperationPointsMap["EURUSD"][1]; !ok {
		expectedResult.ShortOperationPointsMap["EURUSD"][1] = make(map[string]db.ShortOperationPoint)
	}

	expectedResult.LongOperationPointsMap["EURUSD"][1]["2025-01-15"] = longOperationPoints[0]
	expectedResult.LongOperationPointsMap["EURUSD"][1]["2025-01-16"] = longOperationPoints[1]
	expectedResult.ShortOperationPointsMap["EURUSD"][1]["2025-01-15"] = shortOperationPoints[0]
	expectedResult.ShortOperationPointsMap["EURUSD"][1]["2025-01-16"] = shortOperationPoints[1]

	require.ErrorIs(suite.T(), err, nil)
	require.Equal(suite.T(), operationPointsMap, expectedResult, "Maps should match")
}

func (suite *TestSuite) TestGetOperationPointsMapOneInstrumentMultipleStrategies() {
	var longOperationPoints = []db.LongOperationPoint{
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
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-15",
			Result:                    121,
			Tp:                        121,
			Sl:                        80,
			LongBalance:               []int{1000, 1200, 1500},
			Risk:                      0.02,
			MoneyManagementStrategyID: 2,
		},
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-16",
			Result:                    -101,
			Tp:                        200,
			Sl:                        101,
			LongBalance:               []int{1500, 1800, 2000},
			Risk:                      0.01,
			MoneyManagementStrategyID: 2,
		},
	}

	var shortOperationPoints = []db.ShortOperationPoint{
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
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-15",
			Result:                    -121,
			Tp:                        80,
			Sl:                        121,
			ShortBalance:              []int{800, 700, 600},
			Risk:                      0.03,
			MoneyManagementStrategyID: 2,
		},
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-16",
			Result:                    251,
			Tp:                        251,
			Sl:                        150,
			ShortBalance:              []int{2000, 2500, 3000},
			Risk:                      0.02,
			MoneyManagementStrategyID: 2,
		},
	}

	operationPoints := st.OperationPoints{
		LongOperationPoints:  longOperationPoints,
		ShortOperationPoints: shortOperationPoints,
	}
	operationPointsMap, err := st.GetOperationPointsMap(operationPoints)

	expectedResult := st.OperationPointsMaps{
		LongOperationPointsMap:  make(map[string]map[int]map[string]db.LongOperationPoint),
		ShortOperationPointsMap: make(map[string]map[int]map[string]db.ShortOperationPoint),
	}

	if _, ok := expectedResult.LongOperationPointsMap["EURUSD"]; !ok {
		expectedResult.LongOperationPointsMap["EURUSD"] = make(map[int]map[string]db.LongOperationPoint)
	}
	if _, ok := expectedResult.LongOperationPointsMap["EURUSD"][1]; !ok {
		expectedResult.LongOperationPointsMap["EURUSD"][1] = make(map[string]db.LongOperationPoint)
	}
	if _, ok := expectedResult.LongOperationPointsMap["EURUSD"][2]; !ok {
		expectedResult.LongOperationPointsMap["EURUSD"][2] = make(map[string]db.LongOperationPoint)
	}

	if _, ok := expectedResult.ShortOperationPointsMap["EURUSD"]; !ok {
		expectedResult.ShortOperationPointsMap["EURUSD"] = make(map[int]map[string]db.ShortOperationPoint)
	}
	if _, ok := expectedResult.ShortOperationPointsMap["EURUSD"][1]; !ok {
		expectedResult.ShortOperationPointsMap["EURUSD"][1] = make(map[string]db.ShortOperationPoint)
	}
	if _, ok := expectedResult.ShortOperationPointsMap["EURUSD"][2]; !ok {
		expectedResult.ShortOperationPointsMap["EURUSD"][2] = make(map[string]db.ShortOperationPoint)
	}

	expectedResult.LongOperationPointsMap["EURUSD"][1]["2025-01-15"] = longOperationPoints[0]
	expectedResult.LongOperationPointsMap["EURUSD"][1]["2025-01-16"] = longOperationPoints[1]
	expectedResult.LongOperationPointsMap["EURUSD"][2]["2025-01-15"] = longOperationPoints[2]
	expectedResult.LongOperationPointsMap["EURUSD"][2]["2025-01-16"] = longOperationPoints[3]

	expectedResult.ShortOperationPointsMap["EURUSD"][1]["2025-01-15"] = shortOperationPoints[0]
	expectedResult.ShortOperationPointsMap["EURUSD"][1]["2025-01-16"] = shortOperationPoints[1]
	expectedResult.ShortOperationPointsMap["EURUSD"][2]["2025-01-15"] = shortOperationPoints[2]
	expectedResult.ShortOperationPointsMap["EURUSD"][2]["2025-01-16"] = shortOperationPoints[3]

	require.ErrorIs(suite.T(), err, nil)
	require.Equal(suite.T(), operationPointsMap, expectedResult, "Maps should match")
}

func (suite *TestSuite) TestGetOperationPointsMapMultipleInstrumentsMultipleStrategies() {
	var longOperationPoints = []db.LongOperationPoint{
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
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-15",
			Result:                    121,
			Tp:                        121,
			Sl:                        80,
			LongBalance:               []int{1000, 1200, 1500},
			Risk:                      0.02,
			MoneyManagementStrategyID: 2,
		},
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-16",
			Result:                    -101,
			Tp:                        200,
			Sl:                        101,
			LongBalance:               []int{1500, 1800, 2000},
			Risk:                      0.01,
			MoneyManagementStrategyID: 2,
		},

		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-15",
			Result:                    320,
			Tp:                        320,
			Sl:                        80,
			LongBalance:               []int{1000, 1200, 1500},
			Risk:                      0.02,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-16",
			Result:                    -300,
			Tp:                        200,
			Sl:                        300,
			LongBalance:               []int{1500, 1800, 2000},
			Risk:                      0.01,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-15",
			Result:                    321,
			Tp:                        321,
			Sl:                        80,
			LongBalance:               []int{1000, 1200, 1500},
			Risk:                      0.02,
			MoneyManagementStrategyID: 2,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-16",
			Result:                    -301,
			Tp:                        200,
			Sl:                        301,
			LongBalance:               []int{1500, 1800, 2000},
			Risk:                      0.01,
			MoneyManagementStrategyID: 2,
		},
	}

	var shortOperationPoints = []db.ShortOperationPoint{
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
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-15",
			Result:                    -121,
			Tp:                        80,
			Sl:                        121,
			ShortBalance:              []int{800, 700, 600},
			Risk:                      0.03,
			MoneyManagementStrategyID: 2,
		},
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-16",
			Result:                    251,
			Tp:                        251,
			Sl:                        150,
			ShortBalance:              []int{2000, 2500, 3000},
			Risk:                      0.02,
			MoneyManagementStrategyID: 2,
		},

		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-15",
			Result:                    -420,
			Tp:                        80,
			Sl:                        420,
			ShortBalance:              []int{800, 700, 600},
			Risk:                      0.03,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-16",
			Result:                    450,
			Tp:                        450,
			Sl:                        150,
			ShortBalance:              []int{2000, 2500, 3000},
			Risk:                      0.02,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-15",
			Result:                    -521,
			Tp:                        80,
			Sl:                        521,
			ShortBalance:              []int{800, 700, 600},
			Risk:                      0.03,
			MoneyManagementStrategyID: 2,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-16",
			Result:                    651,
			Tp:                        651,
			Sl:                        150,
			ShortBalance:              []int{2000, 2500, 3000},
			Risk:                      0.02,
			MoneyManagementStrategyID: 2,
		},
	}

	operationPoints := st.OperationPoints{
		LongOperationPoints:  longOperationPoints,
		ShortOperationPoints: shortOperationPoints,
	}
	operationPointsMap, err := st.GetOperationPointsMap(operationPoints)

	expectedResult := st.OperationPointsMaps{
		LongOperationPointsMap:  make(map[string]map[int]map[string]db.LongOperationPoint),
		ShortOperationPointsMap: make(map[string]map[int]map[string]db.ShortOperationPoint),
	}

	if _, ok := expectedResult.LongOperationPointsMap["EURUSD"]; !ok {
		expectedResult.LongOperationPointsMap["EURUSD"] = make(map[int]map[string]db.LongOperationPoint)
	}
	if _, ok := expectedResult.LongOperationPointsMap["EURUSD"][1]; !ok {
		expectedResult.LongOperationPointsMap["EURUSD"][1] = make(map[string]db.LongOperationPoint)
	}
	if _, ok := expectedResult.LongOperationPointsMap["EURUSD"][2]; !ok {
		expectedResult.LongOperationPointsMap["EURUSD"][2] = make(map[string]db.LongOperationPoint)
	}

	if _, ok := expectedResult.LongOperationPointsMap["USDCAD"]; !ok {
		expectedResult.LongOperationPointsMap["USDCAD"] = make(map[int]map[string]db.LongOperationPoint)
	}
	if _, ok := expectedResult.LongOperationPointsMap["USDCAD"][1]; !ok {
		expectedResult.LongOperationPointsMap["USDCAD"][1] = make(map[string]db.LongOperationPoint)
	}
	if _, ok := expectedResult.LongOperationPointsMap["USDCAD"][2]; !ok {
		expectedResult.LongOperationPointsMap["USDCAD"][2] = make(map[string]db.LongOperationPoint)
	}

	if _, ok := expectedResult.ShortOperationPointsMap["EURUSD"]; !ok {
		expectedResult.ShortOperationPointsMap["EURUSD"] = make(map[int]map[string]db.ShortOperationPoint)
	}
	if _, ok := expectedResult.ShortOperationPointsMap["EURUSD"][1]; !ok {
		expectedResult.ShortOperationPointsMap["EURUSD"][1] = make(map[string]db.ShortOperationPoint)
	}
	if _, ok := expectedResult.ShortOperationPointsMap["EURUSD"][2]; !ok {
		expectedResult.ShortOperationPointsMap["EURUSD"][2] = make(map[string]db.ShortOperationPoint)
	}

	if _, ok := expectedResult.ShortOperationPointsMap["USDCAD"]; !ok {
		expectedResult.ShortOperationPointsMap["USDCAD"] = make(map[int]map[string]db.ShortOperationPoint)
	}
	if _, ok := expectedResult.ShortOperationPointsMap["USDCAD"][1]; !ok {
		expectedResult.ShortOperationPointsMap["USDCAD"][1] = make(map[string]db.ShortOperationPoint)
	}
	if _, ok := expectedResult.ShortOperationPointsMap["USDCAD"][2]; !ok {
		expectedResult.ShortOperationPointsMap["USDCAD"][2] = make(map[string]db.ShortOperationPoint)
	}

	expectedResult.LongOperationPointsMap["EURUSD"][1]["2025-01-15"] = longOperationPoints[0]
	expectedResult.LongOperationPointsMap["EURUSD"][1]["2025-01-16"] = longOperationPoints[1]
	expectedResult.LongOperationPointsMap["EURUSD"][2]["2025-01-15"] = longOperationPoints[2]
	expectedResult.LongOperationPointsMap["EURUSD"][2]["2025-01-16"] = longOperationPoints[3]

	expectedResult.LongOperationPointsMap["USDCAD"][1]["2025-01-15"] = longOperationPoints[4]
	expectedResult.LongOperationPointsMap["USDCAD"][1]["2025-01-16"] = longOperationPoints[5]
	expectedResult.LongOperationPointsMap["USDCAD"][2]["2025-01-15"] = longOperationPoints[6]
	expectedResult.LongOperationPointsMap["USDCAD"][2]["2025-01-16"] = longOperationPoints[7]

	expectedResult.ShortOperationPointsMap["EURUSD"][1]["2025-01-15"] = shortOperationPoints[0]
	expectedResult.ShortOperationPointsMap["EURUSD"][1]["2025-01-16"] = shortOperationPoints[1]
	expectedResult.ShortOperationPointsMap["EURUSD"][2]["2025-01-15"] = shortOperationPoints[2]
	expectedResult.ShortOperationPointsMap["EURUSD"][2]["2025-01-16"] = shortOperationPoints[3]

	expectedResult.ShortOperationPointsMap["USDCAD"][1]["2025-01-15"] = shortOperationPoints[4]
	expectedResult.ShortOperationPointsMap["USDCAD"][1]["2025-01-16"] = shortOperationPoints[5]
	expectedResult.ShortOperationPointsMap["USDCAD"][2]["2025-01-15"] = shortOperationPoints[6]
	expectedResult.ShortOperationPointsMap["USDCAD"][2]["2025-01-16"] = shortOperationPoints[7]

	require.ErrorIs(suite.T(), err, nil)
	require.Equal(suite.T(), operationPointsMap, expectedResult, "Maps should match")
}
