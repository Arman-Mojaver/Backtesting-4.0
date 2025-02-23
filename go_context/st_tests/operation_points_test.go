package strategy_test

import (
	"database/sql"
	"fmt"
	"os"
	"strategy/db"
	"strategy/st"
	"strategy/fixtures"
	"testing"

	"github.com/stretchr/testify/require"
	"github.com/stretchr/testify/suite"
)

type OperationPointsTestSuite struct {
	suite.Suite
	dbConfig *db.DBConfig
	dbConn   *sql.DB
}

func (suite *OperationPointsTestSuite) SetupSuite() {
	environment := os.Getenv("ENVIRONMENT")
	config, err := db.GetDBConfig(environment)
	require.NoError(suite.T(), err, "Failed to get DB config")

	suite.dbConfig = &config

	fmt.Println("Creating 'testing-db'")
	require.NoError(suite.T(), db.CreateDB(config), "Failed to create database")

	conn, err := db.ConnectDB(config.DBConnStr())
	require.NoError(suite.T(), err, "Failed to connect to database")

	fmt.Println("Creating tables")
	require.NoError(suite.T(), db.CreateTables(conn), "Failed to create tables")

	suite.dbConn = conn
}

func (suite *OperationPointsTestSuite) TearDownTest() {
	require.NoError(suite.T(), db.DeleteEntries(suite.dbConn), "Failed to delete database entries")
}

func (suite *OperationPointsTestSuite) TearDownSuite() {
	require.NoError(suite.T(), suite.dbConn.Close(), "Failed to close database connection")

	fmt.Println("Dropping 'testing-db'")
	require.NoError(suite.T(), db.DropDB(*suite.dbConfig), "Failed to drop database")
}


func (suite *OperationPointsTestSuite) TestGetOperationPointsReturnsEmptyPointsReturnsError() {
	points, err := st.GetOperationPoints(suite.dbConn)
	expectedResult := st.OperationPoints{
		LongOperationPoints: []db.LongOperationPoint{},
		ShortOperationPoints: []db.ShortOperationPoint{},
	}
	require.Equal(suite.T(), points, expectedResult, "Points should match")
	require.ErrorIs(suite.T(), err, st.ErrGetLongOperationPoints)
}

func (suite *OperationPointsTestSuite) TestGetOperationPointsReturnsOnlyShortOperationPointsReturnsError() {
	// Setup
	db.InsertShortOperationPoints(suite.dbConn, fixtures.ShortOperationPoints)

	points, err := st.GetOperationPoints(suite.dbConn)
	expectedResult := st.OperationPoints{
		LongOperationPoints: []db.LongOperationPoint{},
		ShortOperationPoints: []db.ShortOperationPoint{},
	}
	require.Equal(suite.T(), points, expectedResult, "Points should match")
	require.ErrorIs(suite.T(), err, st.ErrGetLongOperationPoints)
}

func (suite *OperationPointsTestSuite) TestGetOperationPointsReturnsOnlyLongOperationPointsReturnsError() {
	// Setup
	db.InsertLongOperationPoints(suite.dbConn, fixtures.LongOperationPoints)

	points, err := st.GetOperationPoints(suite.dbConn)
	expectedResult := st.OperationPoints{
		LongOperationPoints: []db.LongOperationPoint{},
		ShortOperationPoints: []db.ShortOperationPoint{},
	}
	require.Equal(suite.T(), points, expectedResult, "Points should match")
	require.ErrorIs(suite.T(), err, st.ErrGetShortOperationPoints)
}

func (suite *OperationPointsTestSuite) TestGetOperationPointsReturnsOperationPoints() {
	// Setup
	db.InsertLongOperationPoints(suite.dbConn, fixtures.LongOperationPoints)
	db.InsertShortOperationPoints(suite.dbConn, fixtures.ShortOperationPoints)

	points, err := st.GetOperationPoints(suite.dbConn)
	expectedResult := st.OperationPoints{
		LongOperationPoints: fixtures.LongOperationPoints,
		ShortOperationPoints: fixtures.ShortOperationPoints,
	}
	require.Equal(suite.T(), points, expectedResult, "Points should match")
	require.ErrorIs(suite.T(), err, nil)
}

func TestOperationPointsSuite(t *testing.T) {
	os.Setenv("ENVIRONMENT", "testing")
	suite.Run(t, new(OperationPointsTestSuite))
}
