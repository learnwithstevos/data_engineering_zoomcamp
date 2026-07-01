variable "region" {
  description = "Region"
  default     = "us-east-1"
}

variable "a_dataset_name" {
  description = "My athena dataset name"
  default     = "demo-dataset"
}

variable "s3_bucket_name" {
  description = "My s3 bucket name"
  default     = "my-demo-bucket-hw1"
}