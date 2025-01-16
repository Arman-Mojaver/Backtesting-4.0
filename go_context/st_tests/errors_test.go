package strategy_test

import (
	"os"
	"fmt"
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
	config, _ := db.GetDBConfig(environment)

	fmt.Println("Creating 'testing-db'")
	db.CreateDB(config)
}

func (suite *StrategyTestSuite) TearDownTest() {
	// Tear Down test
}

func (suite *StrategyTestSuite) TearDownSuite() {
	environment := os.Getenv("ENVIRONMENT")
	config, _ := db.GetDBConfig(environment)

	fmt.Println("Dropping 'testing-db'")
	db.DropDB(config)
}

func (suite *StrategyTestSuite) TestEnvironmentIsTesting() {
	require.Equal(suite.T(), os.Getenv("ENVIRONMENT"), "testing", "Environment should be 'testing'")
}

func TestErrorsSuite(t *testing.T) {
	os.Setenv("ENVIRONMENT", "testing")
	suite.Run(t, new(StrategyTestSuite))
}
