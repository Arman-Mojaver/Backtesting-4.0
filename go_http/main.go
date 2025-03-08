package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	// Setup logging
	file, err := os.OpenFile("logs/bt.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("Failed to open log file: %s", err)
	}
	defer file.Close()

	multiWriter := io.MultiWriter(os.Stdout, file)
	log.SetOutput(multiWriter)
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	// Setup server
	mux := http.NewServeMux()
	mux.HandleFunc("/", indexHandler)
	mux.HandleFunc("/ping", pingHandler)
	mux.HandleFunc("/process_strategies", processStrategiesHandler)

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

type RequestPayload struct {
    Something  string `json:"something"`
}

func processStrategiesHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		response := map[string]string{"error": "Method Not Allowed"}
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(response)
		return
	}

    var payload RequestPayload
    decoder := json.NewDecoder(r.Body)
	defer r.Body.Close()

    if err := decoder.Decode(&payload); err != nil {
	    response := map[string]string{"error": "Invalid JSON"}
	    w.WriteHeader(http.StatusBadRequest)
	    json.NewEncoder(w).Encode(response)
		return
	}

	response := map[string]string{"message": "success"}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	log.Printf("POST /process_strategies")
}
