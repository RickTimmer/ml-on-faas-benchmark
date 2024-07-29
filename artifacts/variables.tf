variable "aws_region" {
  description = "AWS region to launch servers."
}

variable "aws_user" {
  description = "Name of the AWS user."
}


variable "ecr_id" {
  description = "The ID of the elastic container repository."
}

variable "max_concurrent_executions" {
  description = "Maximum number of concurrent executions of the functions."
}

variable "image_tags" {
  description = "A list of the tags for the Lambda images"
}

variable "memory_sizes" {
  description = "A list of the memory sizes to run"
}

variable "batch_sizes" {
  description = "A list of the batch sizes to be processed"
}

variable "max_messages" {
  description = "A list of the maximum number of messages to be processed"
}

variable "dataset_key" {
  description = "The key to be used to retrieve the dataset from the S3 bucket"
}

locals {
  # Create a list of all possible combinations of image tags and memory sizes, if either is empty the list will be empty
  tag_memory_combinations = length(var.image_tags) > 0 && length(var.memory_sizes) > 0 ? setproduct(split(",", var.image_tags), split(",", var.memory_sizes)) : []
}