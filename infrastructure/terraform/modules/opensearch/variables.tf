# infrastructure/terraform/modules/opensearch/variables.tf
variable "domain_name" {
  description = "Name of the OpenSearch domain"
  type        = string
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
}

variable "instance_type" {
  description = "OpenSearch instance type"
  type        = string
}

variable "instance_count" {
  description = "Number of OpenSearch instances"
  type        = number
}

variable "master_user_name" {
  description = "Master user name for OpenSearch"
  type        = string
}

variable "master_user_password" {
  description = "Master user password for OpenSearch"
  type        = string
  sensitive   = true
}