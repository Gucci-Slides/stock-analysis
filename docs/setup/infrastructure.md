# Infrastructure Setup

## Overview
The project infrastructure consists of:
- S3 Data Lake for raw stock data storage
- OpenSearch for data indexing and querying
- IAM roles and policies for access control

## Components

### S3 Data Lake
- Bucket Name: stock-analysis-data-lake-dev-2025
- Features:
  - Versioning enabled
  - Server-side encryption (AES256)
  - Data organized by: stocks/{symbol}/{date}/data_{period}.json

### OpenSearch Domain
- Domain Name: stock-analysis-dev
- Configuration:
  - Instance Type: t3.small.search
  - Instance Count: 1
  - Storage: 20GB EBS
  - Security: HTTPS enforced, node-to-node encryption

### IAM Configuration
- Role: stock-data-collector-role
- Policies:
  - S3 access for data storage
  - OpenSearch access for indexing

## Terraform Configuration
Infrastructure is managed using Terraform with the following structure:
```bash
infrastructure/terraform/
├── main.tf                 # Main configuration
├── variables.tf            # Variable definitions
├── modules/               
│   ├── s3/                # S3 bucket configuration
│   ├── opensearch/        # OpenSearch domain setup
│   └── iam/               # IAM roles and policies
└── environments/
    └── dev.tfvars         # Development environment variables