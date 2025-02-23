package strategy_test

import (
	"strategy/db"
	"strategy/fixtures"
	"strategy/st"

	"github.com/stretchr/testify/require"
)

func (suite *TestSuite) TestGetOperationPointsReturnsEmptyPointsReturnsError() {
	points, err := st.GetOperationPoints(suite.dbConn)
	expectedResult := st.OperationPoints{
		LongOperationPoints:  []db.LongOperationPoint{},
		ShortOperationPoints: []db.ShortOperationPoint{},
	}
	require.Equal(suite.T(), points, expectedResult, "Points should match")
	require.ErrorIs(suite.T(), err, st.ErrGetLongOperationPoints)
}

func (suite *TestSuite) TestGetOperationPointsReturnsOnlyShortOperationPointsReturnsError() {
	// Setup
	db.InsertShortOperationPoints(suite.dbConn, fixtures.ShortOperationPoints)

	points, err := st.GetOperationPoints(suite.dbConn)
	expectedResult := st.OperationPoints{
		LongOperationPoints:  []db.LongOperationPoint{},
		ShortOperationPoints: []db.ShortOperationPoint{},
	}
	require.Equal(suite.T(), points, expectedResult, "Points should match")
	require.ErrorIs(suite.T(), err, st.ErrGetLongOperationPoints)
}

func (suite *TestSuite) TestGetOperationPointsReturnsOnlyLongOperationPointsReturnsError() {
	// Setup
	db.InsertLongOperationPoints(suite.dbConn, fixtures.LongOperationPoints)

	points, err := st.GetOperationPoints(suite.dbConn)
	expectedResult := st.OperationPoints{
		LongOperationPoints:  []db.LongOperationPoint{},
		ShortOperationPoints: []db.ShortOperationPoint{},
	}
	require.Equal(suite.T(), points, expectedResult, "Points should match")
	require.ErrorIs(suite.T(), err, st.ErrGetShortOperationPoints)
}

func (suite *TestSuite) TestGetOperationPointsReturnsOperationPoints() {
	// Setup
	db.InsertLongOperationPoints(suite.dbConn, fixtures.LongOperationPoints)
	db.InsertShortOperationPoints(suite.dbConn, fixtures.ShortOperationPoints)

	points, err := st.GetOperationPoints(suite.dbConn)
	expectedResult := st.OperationPoints{
		LongOperationPoints:  fixtures.LongOperationPoints,
		ShortOperationPoints: fixtures.ShortOperationPoints,
	}
	require.Equal(suite.T(), points, expectedResult, "Points should match")
	require.ErrorIs(suite.T(), err, nil)
}
