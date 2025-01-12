# Stock Market Analysis System

## Project Structure
- `services/`: Microservices
  - `data_collector/`: Stock data collection service
  - `analyzer/`: Market analysis service
  - `risk_engine/`: Risk assessment service
- `infrastructure/`: IaC configurations
- `lib/`: Shared libraries
- `monitoring/`: Monitoring configurations

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install dependencies for each service
4. Copy `.env.template` to `.env` and configure

## Development
- Each service can be run independently
- Use Docker for local development
- Follow microservices principles
