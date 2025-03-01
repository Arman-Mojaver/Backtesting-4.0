package cmd

import (
	"io"
	"log"
	"os"

	"strategy/db"
	"strategy/st"

	"github.com/spf13/cobra"
)

func init() {
	rootCmd.AddCommand(createCmd)
}

var createCmd = &cobra.Command{
	Use:   "create",
	Short: "Create strategies",
	Run: func(cmd *cobra.Command, args []string) {
		// Setup logging
		file, err := os.OpenFile("bt.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
		if err != nil {
			log.Fatalf("Failed to open log file: %s", err)
		}
		defer file.Close()

		multiWriter := io.MultiWriter(os.Stdout, file)
		log.SetOutput(multiWriter)
		log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

		// Connect to DB
		environment := os.Getenv("ENVIRONMENT")
		config, err := db.GetDBConfig(environment)

		if err != nil {
			log.Fatalf("Error: %v\n", err)
			return
		}
		log.Printf("DBConfig: %+v\n", config)

		conn, err := db.ConnectDB(config.DBConnStr())
		if err != nil {
			log.Fatalf("Cannot reach the database: %v", err)
			return
		}
		defer conn.Close()
		log.Println("Connected to PostgreSQL!")

		// Query operation points
		operationPoints, err := st.GetOperationPoints(conn)
		if err != nil {
			log.Fatalf("Error in Querying Operation Points: %v", err)
			return
		}
		log.Printf("Queried OperationPoints successfully!")

		operationPointsMap, err := st.GetOperationPointsMap(operationPoints)
		if err != nil {
			log.Fatalf("Error creating Operation Points Map: %v", err)
			return
		}
		_ = operationPointsMap
		// log.Println(operationPointsMap.LongOperationPointsMap["EURUSD"][382541]["2015-05-01"])
		log.Printf("Created OperationPointsMap successfully!")

		// log.Println("Created strategies")
	},
}
