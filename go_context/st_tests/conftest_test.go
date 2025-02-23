package strategy_test

import (
	"database/sql"
	"fmt"
	"os"
	"strategy/db"
	"testing"

	"github.com/stretchr/testify/require"
	"github.com/stretchr/testify/suite"
)

type TestSuite struct {
	suite.Suite
	dbConfig *db.DBConfig
	dbConn   *sql.DB
}

func (suite *TestSuite) SetupSuite() {
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

func (suite *TestSuite) TearDownTest() {
	require.NoError(suite.T(), db.DeleteEntries(suite.dbConn), "Failed to delete database entries")
}

func (suite *TestSuite) TearDownSuite() {
	require.NoError(suite.T(), suite.dbConn.Close(), "Failed to close database connection")

	fmt.Println("Dropping 'testing-db'")
	require.NoError(suite.T(), db.DropDB(*suite.dbConfig), "Failed to drop database")
}

func (suite *TestSuite) TestEnvironmentIsTesting() {
	require.Equal(suite.T(), os.Getenv("ENVIRONMENT"), "testing", "Environment should be 'testing'")
}

func TestStSuite(t *testing.T) {
	os.Setenv("ENVIRONMENT", "testing")
	suite.Run(t, new(TestSuite))
}
