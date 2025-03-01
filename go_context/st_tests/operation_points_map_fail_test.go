package strategy_test

import (
	"strategy/db"
	"strategy/st"

	"github.com/stretchr/testify/require"
)

func (suite *TestSuite) TestGetOperationPointsMapReturnsHasLengthMismatchError() {
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
	expectedResult := st.OperationPointsMaps{}

	require.ErrorIs(suite.T(), err, st.ErrOperationPointsMismatch)
	require.Equal(suite.T(), operationPointsMap, expectedResult, "Maps should match")
}

func (suite *TestSuite) TestGetOperationPointsMapReturnsReturnsDateMismatchOneInstrumentError() {
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
			Datetime:                  "2025-01-17",
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
	expectedResult := st.OperationPointsMaps{}

	require.ErrorIs(suite.T(), err, st.ErrOperationPointsMismatch)
	require.Equal(suite.T(), operationPointsMap, expectedResult, "Maps should match")
}

func (suite *TestSuite) TestGetOperationPointsMapReturnsReturnsDateMismatchSeveralInstrumentError() {
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
			Datetime:                  "2025-01-17",
			Result:                    -100,
			Tp:                        200,
			Sl:                        100,
			LongBalance:               []int{1500, 1800, 2000},
			Risk:                      0.01,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-21",
			Result:                    120,
			Tp:                        120,
			Sl:                        80,
			LongBalance:               []int{1000, 1200, 1500},
			Risk:                      0.02,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-22",
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
			Datetime:                  "2025-01-22",
			Result:                    250,
			Tp:                        250,
			Sl:                        150,
			ShortBalance:              []int{2000, 2500, 3000},
			Risk:                      0.02,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "EURUSD",
			Datetime:                  "2025-01-17",
			Result:                    -100,
			Tp:                        200,
			Sl:                        100,
			ShortBalance:              []int{1500, 1800, 2000},
			Risk:                      0.01,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "USDCAD",
			Datetime:                  "2025-01-21",
			Result:                    -120,
			Tp:                        80,
			Sl:                        120,
			ShortBalance:              []int{800, 700, 600},
			Risk:                      0.03,
			MoneyManagementStrategyID: 1,
		},
		{
			Instrument:                "USDCAD",
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
	expectedResult := st.OperationPointsMaps{}

	require.ErrorIs(suite.T(), err, st.ErrOperationPointsMismatch)
	require.Equal(suite.T(), operationPointsMap, expectedResult, "Maps should match")
}
