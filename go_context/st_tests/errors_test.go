package strategy_test

import (
	"fmt"
	"os"
	"strategy/db"
	"testing"

	"github.com/stretchr/testify/require"
	"github.com/stretchr/testify/suite"
)

type StrategyTestSuite struct {
	suite.Suite
}

func (suite *StrategyTestSuite) SetupSuite() {
	environment := os.Getenv("ENVIRONMENT")
	config, err := db.GetDBConfig(environment)
	require.NoError(suite.T(), err, "Failed to get DB config")

	fmt.Println("Creating 'testing-db'")
	require.NoError(suite.T(), db.CreateDB(config), "Failed to create database")

	conn, err := db.ConnectDB(config.DBConnStr())
	require.NoError(suite.T(), err, "Failed to connect to database")
	defer conn.Close()

	fmt.Println("Creating tables")
	require.NoError(suite.T(), db.CreateTables(conn), "Failed to create tables")

}

func (suite *StrategyTestSuite) TearDownTest() {
	// Tear Down test
}

func (suite *StrategyTestSuite) TearDownSuite() {
	environment := os.Getenv("ENVIRONMENT")
	config, err := db.GetDBConfig(environment)
	require.NoError(suite.T(), err, "Failed to get DB config")

	fmt.Println("Dropping 'testing-db'")
	require.NoError(suite.T(), db.DropDB(config), "Failed to drop database")

}

func (suite *StrategyTestSuite) TestEnvironmentIsTesting() {
	require.Equal(suite.T(), os.Getenv("ENVIRONMENT"), "testing", "Environment should be 'testing'")
}

func TestErrorsSuite(t *testing.T) {
	os.Setenv("ENVIRONMENT", "testing")
	suite.Run(t, new(StrategyTestSuite))
}
