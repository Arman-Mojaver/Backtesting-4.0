package ps

import (
	"runtime"
	"sync"
)

func ProcessStrategies(payload *RequestPayload) []StrategyItem {
	cpuCount := runtime.NumCPU()
	workerMultiplier := 1
	workerCount := cpuCount * workerMultiplier
	inputChannelBufferSize := 10000
	outputChannelBufferSize := 10000

	inputCh := make(chan ProcessData, inputChannelBufferSize)
	outputCh := make(chan StrategyItem, outputChannelBufferSize)
	var wg sync.WaitGroup

	sendToInputChannel(payload, inputCh)
	receiveFromInputChannelAndSendToOutputChannel(inputCh, outputCh, workerCount, &wg)
	waitForResults(outputCh, &wg)
	strategyItems := collectResults(outputCh)

	return strategyItems
}

func sendToInputChannel(
	payload *RequestPayload,
	inputCh chan ProcessData,
) {
	go func() {
		for moneyManagementStrategyID, operationPoints := range payload.OperationPoints {
			for indicatorID, signals := range payload.Signals {
				item := ProcessData{"EURUSD", moneyManagementStrategyID, indicatorID, operationPoints, signals, payload.StartDate, payload.EndDate}
				inputCh <- item
			}
		}
		close(inputCh)
	}()
}

func receiveFromInputChannelAndSendToOutputChannel(
	inputCh chan ProcessData,
	outputCh chan StrategyItem,
	workerCount int,
	wg *sync.WaitGroup,
) {
	for i := 0; i < workerCount; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for item := range inputCh {
				result := process(item)
				outputCh <- result
			}
		}()
	}
}

func waitForResults(outputCh chan StrategyItem, wg *sync.WaitGroup) {
	go func() {
		wg.Wait()
		close(outputCh)
	}()
}

func collectResults(outputCh chan StrategyItem) []StrategyItem {
	var strategyItems []StrategyItem
	for result := range outputCh {
		strategyItems = append(strategyItems, result)
	}
	return strategyItems
}
