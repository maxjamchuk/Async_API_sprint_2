import uuid

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from tests.functional.settings import test_settings

#  Название теста должно начинаться со слова `test_`
#  Любой тест с асинхронными вызовами нужно оборачивать декоратором `pytest.mark.asyncio`, который следит за запуском и работой цикла событий. 

@pytest.mark.asyncio
async def test_search():

    # 1. Генерируем данные для ES

    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_raiting': 8.5,
        'genres': [
            {'id': '000', 'name': 'Action'},
            {'id': '001', 'name': 'Sci-Fi'}
        ],
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
        'directors': [
            {'id': '555', 'name': 'Stan'},
        ],
    } for _ in range(60)]
     
    bulk_query = []
    for row in es_data:
        bulk_query.append(
                {'_index': 'movies', '_id': row.get('id'), '_source' : row}
        ) 

    # 2. Загружаем данные в ES

    es_client = AsyncElasticsearch(hosts=[f'http://{test_settings.elastic_host}:{test_settings.elastic_port}'])
    response = await async_bulk(es_client, bulk_query)

    await es_client.close()
    
    # 3. Запрашиваем данные из ES по API

    session = aiohttp.ClientSession()
    url = f'http://service:8000/api/v1/films/search'
    query_data = {'query': 'The Star', 'page_number': 1, 'page_size': 50}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    # 4. Проверяем ответ 

    assert status == 200
    assert len(body) == 50 