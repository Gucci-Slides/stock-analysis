# infrastructure/terraform/variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
}

variable "data_lake_bucket_name" {
  description = "Name of the S3 bucket for data lake"
  type        = string
}

variable "opensearch_domain_name" {
  description = "Name of the OpenSearch domain"
  type        = string
}

variable "opensearch_instance_type" {
  description = "OpenSearch instance type"
  type        = string
  default     = "t3.small.search"
}

variable "opensearch_instance_count" {
  description = "Number of OpenSearch instances"
  type        = number
  default     = 2
}

variable "opensearch_master_user_name" {
  description = "Master user name for OpenSearch"
  type        = string
  default     = "admin"
}

variable "opensearch_master_user_password" {
  description = "Master user password for OpenSearch"
  type        = string
  sensitive   = true
}