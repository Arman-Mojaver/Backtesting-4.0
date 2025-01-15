package strategy_test

import (
	"os"
	"testing"

	"github.com/stretchr/testify/suite"
	"github.com/stretchr/testify/require"
)


type StrategyTestSuite struct {
	suite.Suite
}

func (suite *StrategyTestSuite) SetupSuite() {
	// Setup suite
}


func (suite *StrategyTestSuite) TearDownTest() {
	// Tear Down test
}


func (suite *StrategyTestSuite) TearDownSuite() {
	// Tear Down suite
}


func (suite *StrategyTestSuite) TestEnvironmentIsTesting() {
	require.Equal(suite.T(), os.Getenv("ENVIRONMENT"), "testing", "Environment should be 'testing'")
}


func TestErrorsSuite(t *testing.T) {
	os.Setenv("ENVIRONMENT", "testing")
	suite.Run(t, new(StrategyTestSuite))
}
