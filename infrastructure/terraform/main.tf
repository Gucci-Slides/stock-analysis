# infrastructure/terraform/main.tf
provider "aws" {
  region = var.aws_region
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  backend "s3" {
    bucket = "stock-analysis-terraform-state-auon1nwb"
    key    = "stock-analysis/terraform.tfstate"
    region = "us-east-1"
  }
}

# S3 Data Lake
module "data_lake" {
  source      = "./modules/s3"
  bucket_name = var.data_lake_bucket_name
  environment = var.environment
}

# OpenSearch (Elasticsearch)
module "opensearch" {
  source          = "./modules/opensearch"
  domain_name     = var.opensearch_domain_name
  environment     = var.environment
  instance_type   = var.opensearch_instance_type
  instance_count  = var.opensearch_instance_count
  master_user_name = var.opensearch_master_user_name
  master_user_password = var.opensearch_master_user_password
}

# IAM roles and policies
module "iam" {
  source = "./modules/iam"
  data_lake_bucket_name = module.data_lake.bucket_name
  opensearch_domain_arn = module.opensearch.domain_arn
  environment = var.environment
}