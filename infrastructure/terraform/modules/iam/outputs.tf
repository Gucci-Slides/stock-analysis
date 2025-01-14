# infrastructure/terraform/modules/iam/outputs.tf
output "collector_role_arn" {
  description = "ARN of the stock data collector IAM role"
  value       = aws_iam_role.stock_data_collector.arn
}