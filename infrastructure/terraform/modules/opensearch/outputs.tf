# infrastructure/terraform/modules/opensearch/outputs.tf
output "domain_arn" {
  description = "ARN of the OpenSearch domain"
  value       = aws_opensearch_domain.stock_data.arn
}