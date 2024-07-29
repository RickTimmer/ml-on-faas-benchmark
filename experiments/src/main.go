package main

import (
	"encoding/csv"
	"encoding/json"
	"log"
	"strconv"
	"strings"

	"github.com/google/uuid"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/sns"

	"os"
)

var logger = log.New(os.Stdout, "[Experiments] ", log.Ldate|log.Lmicroseconds)

type Experiment struct {
	id        string
	topicARN  string
	batchSize int
	batches   [][]string
	snsSvc    *sns.SNS
}

type Message struct {
	ExperimentId string
	MessageId    string
	Batch        []string
}

func main() {

	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))
	experimentId := uuid.New().String()

	logger.Println("Retrieving data for experiment: ", experimentId)
	items := getDataset(sess)

	logger.Println("Number of questions: ", len(items))

	logger.Println("Starting experiment: ", experimentId)

	maxMessages, _ := strconv.Atoi(os.Getenv("MAX_MESSAGES"))
	batchSizes := getBatchSizes()

	for _, batchSize := range batchSizes {
		logger.Println("Dividing dataset into batches of size ", batchSize)
		batches := createBatches(batchSize, maxMessages, items)
		experiment := NewExperiment(sess, experimentId, batchSize, batches)
		experiment.publishBatches()
	}
}

func getBatchSizes() []int {
	batchSizes := strings.Split(os.Getenv("BATCH_SIZES"), ",")
	var batchSizesInt []int
	for _, batchSize := range batchSizes {
		batchSizeInt, err := strconv.Atoi(batchSize)
		if err != nil {
			logger.Fatal("Error converting batch size to int:", err)
		}
		batchSizesInt = append(batchSizesInt, batchSizeInt)
	}
	return batchSizesInt
}

func createBatches(batchSize int, maxMessages int, items []string) [][]string {

	// Create a 2D slice to hold the batches
	batches := make([][]string, maxMessages)

	for i := 0; i < maxMessages; i++ {
		batch := make([]string, batchSize)

		for j := 0; j < batchSize; j++ {
			// Calculate the index in the items array, wrapping around if necessary
			index := (i*batchSize + j) % len(items)
			batch[j] = items[index]
		}
		logger.Printf("Batch %d is of length %d.\n", i, len(batch))

		batches[i] = batch
	}
	logger.Printf("Created %d batches.\n", len(batches))

	return batches
}

func NewExperiment(sess *session.Session, experimentId string, batchSize int, batches [][]string) Experiment {

	snsSvc := sns.New(sess)

	return Experiment{
		id:        experimentId,
		snsSvc:    snsSvc,
		topicARN:  getARN(snsSvc),
		batchSize: batchSize,
		batches:   batches,
	}
}

func getDataset(sess *session.Session) []string {
	s3Svc := s3.New(sess)

	bucket := "ml-on-faas-bucket"
	key := os.Getenv("DATASET_KEY")

	result, err := s3Svc.GetObject(&s3.GetObjectInput{
		Bucket: aws.String(bucket),
		Key:    aws.String(key),
	})

	if err != nil {
		logger.Fatal("Error getting object:", err)
	}

	// Read the object content
	body := result.Body
	defer body.Close()

	// Parse the CSV content
	reader := csv.NewReader(body)
	records, err := reader.ReadAll()
	if err != nil {
		logger.Fatal("Error reading CSV:", err)
	}

	var messages []string

	if key == "llm_dataset.csv" {
		for _, record := range records {
			if len(record) >= 11 { // Ensure there are enough columns
				messages = append(messages, record[9]) // Index 9 corresponds to the "question" column
			}
		}
	} else if key == "sentiment.csv" {
		for _, record := range records {
			if len(record) >= 2 { // Ensure there are enough columns
				messages = append(messages, record[1]) // Index 1 corresponds to the "text" column
			}
		}
	} else {
		logger.Fatal("Experiment container does not know how to handle dataset with key:", key)
		os.Exit(1)
	}

	return messages
}

func (experiment Experiment) publishBatches() {
	logger.Println("Starting batch of size ", experiment.batchSize, " for experiment: ", experiment.id)
	maxMessages, _ := strconv.Atoi(os.Getenv("MAX_MESSAGES"))
	for i, batch := range experiment.batches {
		if i >= maxMessages {
			logger.Println("Limit of", i, "messages reached.")
			break
		}

		messageId := uuid.New().String()
		message := Message{
			ExperimentId: experiment.id,
			MessageId:    messageId,
			Batch:        batch,
		}

		jsonString, _ := json.Marshal(message)

		logger.Println("Publishing message ", messageId)
		result, err := experiment.snsSvc.Publish(&sns.PublishInput{
			Message:  aws.String(string(jsonString)),
			TopicArn: &experiment.topicARN,
		})
		if err != nil {
			logger.Fatal(err.Error())
			os.Exit(1)
		}
		logger.Println("Published message ", messageId, " with message ID ", *result.MessageId)
	}
}

func getARN(svc *sns.SNS) string {
	var topicARN string
	topicFilter := "ml-on-faas-sns-topic"

	// Get the list of topics
	topicsOutput, err := svc.ListTopics(nil)
	if err != nil {
		logger.Fatal("Error listing SNS topics:", err.Error())
		os.Exit(1)
	}

	// Check if the topic's ARN contains the specified filter
	for _, topic := range topicsOutput.Topics {
		if strings.Contains(*topic.TopicArn, topicFilter) {
			topicARN = *topic.TopicArn
			break
		}
	}

	if topicARN == "" {
		logger.Fatal("No SNS topic found matching the filter:", topicFilter)
		os.Exit(1)
	}

	return topicARN
}
