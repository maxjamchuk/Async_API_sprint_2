import pytest
import aiohttp

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from tests.functional.settings import test_settings
from typing import List


def get_es_bulk_query(data: List[dict], index: str) -> List[dict]:
    bulk_query = []
    for row in data:
        bulk_query.append(
                {'_index': index, '_id': row.get('id'), '_source': row}
        )
    return bulk_query

@pytest.fixture(scope='session')
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope='session')
async def http_client():
    async with aiohttp.ClientSession() as client:
        yield client

@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=[f'http://{test_settings.elastic_host}:{test_settings.elastic_port}'])
    yield client
    await client.close()

@pytest.fixture(scope='function')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: List[dict], index: str):
        bulk_query = get_es_bulk_query(data, index)
        await async_bulk(es_client, bulk_query, refresh=True)
    return inner

@pytest.fixture(scope='function')
def make_get_request(http_client: aiohttp.ClientSession):
    async def inner(query: str, params: dict):
        response = await http_client.get(query, params=params)
        return response
    return inner 