package strategy_test

import (
	"database/sql"
	"fmt"
	"os"
	"strategy/db"
	"strategy/fixtures"
	"testing"

	"github.com/stretchr/testify/require"
	"github.com/stretchr/testify/suite"
)

type StrategyTestSuite struct {
	suite.Suite
	dbConfig *db.DBConfig
	dbConn   *sql.DB
}

func (suite *StrategyTestSuite) SetupSuite() {
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

func (suite *StrategyTestSuite) TearDownTest() {
	require.NoError(suite.T(), db.DeleteEntries(suite.dbConn), "Failed to delete database entries")
}

func (suite *StrategyTestSuite) TearDownSuite() {
	require.NoError(suite.T(), suite.dbConn.Close(), "Failed to close database connection")

	fmt.Println("Dropping 'testing-db'")
	require.NoError(suite.T(), db.DropDB(*suite.dbConfig), "Failed to drop database")
}

func (suite *StrategyTestSuite) TestEnvironmentIsTesting() {
	require.Equal(suite.T(), os.Getenv("ENVIRONMENT"), "testing", "Environment should be 'testing'")
}

func (suite *StrategyTestSuite) TestGetLongOperationPointsNoLongOperationPoints() {
	points, err := db.GetLongOperationPoints(suite.dbConn)
	require.Equal(suite.T(), err, db.ErrorNoLongOperationPoints, "Error should be ErrorNoLongOperationPoints")
	require.Equal(suite.T(), points, []db.LongOperationPoint{}, "Slice should be empty")
}

func (suite *StrategyTestSuite) TestGetLongOperationPointsReturnsPoints() {
	// Setup
	db.InsertLongOperationPoints(suite.dbConn, fixtures.LongOperationPoints)

	points, err := db.GetLongOperationPoints(suite.dbConn)
	require.Equal(suite.T(), err, nil, "Error should be nil")
	require.Equal(suite.T(), points, fixtures.LongOperationPoints, "Points should match")
}

func (suite *StrategyTestSuite) TestGetShortOperationPointsNoShortOperationPoints() {
	points, err := db.GetShortOperationPoints(suite.dbConn)
	require.Equal(suite.T(), err, db.ErrorNoShortOperationPoints, "Error should be ErrorNoShortOperationPoints")
	require.Equal(suite.T(), points, []db.ShortOperationPoint{}, "Slice should be empty")
}

func (suite *StrategyTestSuite) TestGetShortOperationPointsReturnsPoints() {
	// Setup
	db.InsertShortOperationPoints(suite.dbConn, fixtures.ShortOperationPoints)

	points, err := db.GetShortOperationPoints(suite.dbConn)
	require.Equal(suite.T(), err, nil, "Error should be nil")
	require.Equal(suite.T(), points, fixtures.ShortOperationPoints, "Points should match")
}

func TestErrorsSuite(t *testing.T) {
	os.Setenv("ENVIRONMENT", "testing")
	suite.Run(t, new(StrategyTestSuite))
}
