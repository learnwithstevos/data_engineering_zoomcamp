terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "hw1_demo" {
  bucket        = var.s3_bucket_name
  force_destroy = true
}

resource "aws_athena_workgroup" "hw1_demo-dataset" {
  name = var.a_dataset_name

  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.hw1_demo.bucket}/athena-results/"
    }
  }
}