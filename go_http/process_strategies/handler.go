package ps

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

func ProcessStrategiesHandler(w http.ResponseWriter, r *http.Request) {
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

	log.Printf("Starting to process strategies")
	start := time.Now()
	strategyItems := ProcessStrategies(&payload)
	response := Response{Data: strategyItems}

	elapsed := time.Since(start)
	log.Printf("Finished to process strategies. Elapsed time: %s", elapsed)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)

	log.Printf("POST /process_strategies")
}
