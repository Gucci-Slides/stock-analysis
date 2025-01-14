# test_infrastructure.py
import boto3
import yfinance as yf
from opensearchpy import OpenSearch, RequestsHttpConnection
from datetime import datetime

def test_s3_upload():
    # Get some test data
    ticker = yf.Ticker("AAPL")
    hist = ticker.history(period="1d")
    test_data = hist.to_json()

    # Upload to S3
    s3 = boto3.client('s3')
    bucket_name = 'stock-analysis-data-lake-dev-2025'
    key = f'test/AAPL/{datetime.now().strftime("%Y/%m/%d")}/data.json'

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=test_data
        )
        print(f"Successfully uploaded test data to S3: s3://{bucket_name}/{key}")
    except Exception as e:
        print(f"Error uploading to S3: {str(e)}")

def test_opensearch_connection():
    opensearch = boto3.client('opensearch')
    domain_name = 'stock-analysis-dev'
    
    try:
        domain_info = opensearch.describe_domain(DomainName=domain_name)
        endpoint = domain_info['DomainStatus']['Endpoint']
        
        print(f"OpenSearch Endpoint: {endpoint}")
        
        # Connect to OpenSearch with authentication
        os_client = OpenSearch(
            hosts = [{'host': endpoint, 'port': 443}],
            http_auth = ('admin', 'password'), 
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )

        # Test index creation
        index_name = 'test-index'
        os_client.indices.create(index=index_name, ignore=400)
        
        # Test document indexing
        doc = {
            'title': 'Test Document',
            'timestamp': datetime.now().isoformat()
        }
        response = os_client.index(
            index=index_name,
            body=doc,
            refresh=True
        )
        
        print("Successfully connected to OpenSearch and indexed test document")
        
    except Exception as e:
        print(f"Error connecting to OpenSearch: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing S3 upload...")
    test_s3_upload()
    
    print("\nTesting OpenSearch connection...")
    test_opensearch_connection()