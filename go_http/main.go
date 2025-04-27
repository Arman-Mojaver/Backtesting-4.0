package main

import (
	"encoding/json"
	"go_http/indicators/rsi"
	"go_http/process_strategies"
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	// Setup logging
	file, err := os.OpenFile("logs/go-http.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("Failed to open log file: %s", err)
	}
	defer file.Close()

	multiWriter := io.MultiWriter(os.Stdout, file)
	log.SetOutput(multiWriter)
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	// Setup server
	mux := http.NewServeMux()

	// General Handlers
	mux.HandleFunc("/", indexHandler)
	mux.HandleFunc("/ping", pingHandler)

	// Custom Handlers
	mux.HandleFunc("/process_strategies", ps.ProcessStrategiesHandler)

	// Indicator Handlers
	mux.HandleFunc("/rsi", rsi.RSIHandler)

	log.Println("Server starting on port 80...")
	log.Fatal(http.ListenAndServe(":80", mux))
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"message": "Server Working. Endpoint not defined!"}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"message": "Ping!"}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	log.Println("GET /ping")
}
