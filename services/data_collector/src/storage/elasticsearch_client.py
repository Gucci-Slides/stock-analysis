# services/data_collector/src/storage/elasticsearch_client.py
from elasticsearch import AsyncElasticsearch
from datetime import datetime

class ElasticsearchClient:
    def __init__(self, hosts: list):
        self.es = AsyncElasticsearch(hosts=hosts)
        self.index_name = 'stock_data'

    async def store_stock_data(self, symbol: str, data: dict):
        # Add metadata
        document = {
            'symbol': symbol,
            'timestamp': datetime.now(),
            'data': data
        }
        
        try:
            await self.es.index(
                index=self.index_name,
                document=document,
                id=f"{symbol}_{datetime.now().strftime('%Y%m%d')}"
            )
        except Exception as e:
            raise Exception(f"Failed to store data in Elasticsearch: {str(e)}")

    async def search_stock_data(self, symbol: str, start_date: str = None, end_date: str = None):
        query = {
            'bool': {
                'must': [
                    {'match': {'symbol': symbol}}
                ]
            }
        }
        
        if start_date and end_date:
            query['bool']['must'].append({
                'range': {
                    'timestamp': {
                        'gte': start_date,
                        'lte': end_date
                    }
                }
            })

        try:
            result = await self.es.search(
                index=self.index_name,
                query=query,
                size=100
            )
            return result['hits']['hits']
        except Exception as e:
            raise Exception(f"Failed to search Elasticsearch: {str(e)}")