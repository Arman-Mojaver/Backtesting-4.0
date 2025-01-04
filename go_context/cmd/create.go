package cmd

import (
  "fmt"

  "github.com/spf13/cobra"
)

func init() {
  rootCmd.AddCommand(createCmd)
}

var createCmd = &cobra.Command{
  Use:   "create",
  Short: "Create strategies",
  Run: func(cmd *cobra.Command, args []string) {
    fmt.Println("Created strategies")
  },
}
