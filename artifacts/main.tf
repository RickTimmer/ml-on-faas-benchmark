terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.44"
    }
  }
  backend "s3" {
    bucket         = <BUCKET>
    key            = <KEY>
    region         = <REGION>
  }
}

provider "aws" {
  region = var.aws_region
}
