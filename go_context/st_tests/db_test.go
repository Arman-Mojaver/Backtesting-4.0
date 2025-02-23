package strategy_test

import (
	"strategy/db"
	"strategy/fixtures"

	"github.com/stretchr/testify/require"
)

func (suite *TestSuite) TestGetLongOperationPointsNoLongOperationPoints() {
	points, err := db.GetLongOperationPoints(suite.dbConn)
	require.Equal(suite.T(), err, db.ErrorNoLongOperationPoints, "Error should be ErrorNoLongOperationPoints")
	require.Equal(suite.T(), points, []db.LongOperationPoint{}, "Slice should be empty")
}

func (suite *TestSuite) TestGetLongOperationPointsReturnsPoints() {
	// Setup
	db.InsertLongOperationPoints(suite.dbConn, fixtures.LongOperationPoints)

	points, err := db.GetLongOperationPoints(suite.dbConn)
	require.Equal(suite.T(), err, nil, "Error should be nil")
	require.Equal(suite.T(), points, fixtures.LongOperationPoints, "Points should match")
}

func (suite *TestSuite) TestGetShortOperationPointsNoShortOperationPoints() {
	points, err := db.GetShortOperationPoints(suite.dbConn)
	require.Equal(suite.T(), err, db.ErrorNoShortOperationPoints, "Error should be ErrorNoShortOperationPoints")
	require.Equal(suite.T(), points, []db.ShortOperationPoint{}, "Slice should be empty")
}

func (suite *TestSuite) TestGetShortOperationPointsReturnsPoints() {
	// Setup
	db.InsertShortOperationPoints(suite.dbConn, fixtures.ShortOperationPoints)

	points, err := db.GetShortOperationPoints(suite.dbConn)
	require.Equal(suite.T(), err, nil, "Error should be nil")
	require.Equal(suite.T(), points, fixtures.ShortOperationPoints, "Points should match")
}
