package cmd

import (
	"fmt"
	"os"

	"strategy/db"

	"github.com/spf13/cobra"
)

func init() {
	rootCmd.AddCommand(createCmd)
}

var createCmd = &cobra.Command{
	Use:   "create",
	Short: "Create strategies",
	Run: func(cmd *cobra.Command, args []string) {
		environment := os.Getenv("ENVIRONMENT")
		config, err := db.GetDBConfig(environment)

		if err != nil {
			fmt.Printf("Error: %v\n", err)
			return
		}
		fmt.Printf("DBConfig: %+v\n", config)

		conn, err := db.ConnectDB(config.DBConnStr())
		if err != nil {
			fmt.Printf("Cannot reach the database: %v", err)
			return
		}
		defer conn.Close()
		fmt.Println("Connected to PostgreSQL!")

		// fmt.Println("Created strategies")
	},
}
