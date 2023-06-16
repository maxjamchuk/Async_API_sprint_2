import uuid
import pytest

from tests.functional.settings import test_settings

@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'query': 'The Star', 'page_number': 1, 'page_size': 50},
                {'status': 200, 'length': 50}
        ),
        (
                {'query': 'Mashed potato', 'page_number': 1, 'page_size': 50},
                {'status': 404, 'length': 1}
        )
    ]
)
@pytest.mark.anyio
async def test_search(make_get_request, es_write_data, query_data, expected_answer):

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
     
    await es_write_data(data=es_data, index='movies')
    response = await make_get_request('http://service:8000/api/v1/films/search', params=query_data)
    
    assert response.status == expected_answer.get('status')
    assert len(await response.json()) == expected_answer.get('length')