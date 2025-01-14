# infrastructure/terraform/modules/iam/variables.tf
variable "data_lake_bucket_name" {
  description = "Name of the S3 bucket for data lake"
  type        = string
}

variable "opensearch_domain_arn" {
  description = "ARN of the OpenSearch domain"
  type        = string
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
}