package db

import "fmt"

type DBConfig struct {
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
	SSLMode  string
}

func (cfg *DBConfig) ConnStr() string {
	return fmt.Sprintf("host=%s port=%d user=%s password=%s sslmode=%s",
		cfg.Host, cfg.Port, cfg.User, cfg.Password, cfg.SSLMode)
}

func (cfg *DBConfig) DBConnStr() string {
	return fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
		cfg.Host, cfg.Port, cfg.User, cfg.Password, cfg.DBName, cfg.SSLMode)
}

// Table structs

type ResampledPointD1 struct {
	ID           int64
	Datetime     string
	Instrument   string
	Open         float64
	High         float64
	Low          float64
	Close        float64
	Volume       int
	HighLowOrder string
}

type LongOperationPoint struct {
	ID                        int64
	Instrument                string
	Datetime                  string
	Result                    int
	Tp                        int
	Sl                        int
	LongBalance               []int
	Risk                      float64
	MoneyManagementStrategyID int
}

type ShortOperationPoint struct {
	ID                        int64
	Instrument                string
	Datetime                  string
	Result                    int
	Tp                        int
	Sl                        int
	ShortBalance              []int
	Risk                      float64
	MoneyManagementStrategyID int
}

type Indicator struct {
	ID         int64
	Type       string
	Parameters string
	Identifier string
}

type Strategy struct {
	ID                        int64
	AnnualROI                 float64
	MaxDrawDown               float64
	MinAnnualROI              float64
	AnnualOperationCount      float64
	MoneyManagementStrategyID int
	IndicatorID               int
}
