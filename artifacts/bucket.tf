resource "aws_s3_bucket" "ml_on_faas_bucket" {
  bucket = "ml-on-faas-bucket"
}

resource "aws_s3_object" "ml_on_faas_llm_dataset" {
  bucket = aws_s3_bucket.ml_on_faas_bucket.id
  key    = "llm_dataset.csv"
  source = "../datasets/ARC-Challenge-Train.csv"
}

resource "aws_s3_object" "ml_on_faas_sentiment_dataset" {
  bucket = aws_s3_bucket.ml_on_faas_bucket.id
  key    = "sentiment.csv"
  source = "../datasets/sentiment.csv"
}
