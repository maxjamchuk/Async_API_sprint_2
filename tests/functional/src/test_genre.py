import uuid
import pytest

from typing import Coroutine, Dict, Union

from ..settings import test_settings as sett
from ..testdata.genre import (
    UUIDS_GENRES,
    ES_GENRE_GEN_DATA,
    ES_GENRES_PARAMETRIZE_POSITIVE_DATA,
    ES_GENRES_PARAMETRIZE_NEGATIVE_DATA,
    ES_GENRE_BY_ID_PARAMETRIZE_POSITIVE_DATA,
    ES_GENRE_BY_ID_PARAMETRIZE_NEGATIVE_DATA
)

@pytest.mark.parametrize(
    'query_data, expected_answer',
    ES_GENRES_PARAMETRIZE_POSITIVE_DATA + ES_GENRES_PARAMETRIZE_NEGATIVE_DATA
)

@pytest.mark.anyio
async def test_get_all_genres(
	make_get_request: Coroutine,
	es_write_data: Coroutine,
	query_data: Dict[str, Union[str, int, float, None]],
	expected_answer: Dict[str, Union[str, int, float, None]],
):


	url = f'{sett.app_api_host}genres'
	response = await make_get_request(url, params=query_data)
	data_response = await response.json()

	assert response.status == expected_answer.get('status')
	assert len(data_response) == expected_answer.get('length')
	if response.status == 422:
		assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')

	if 'full_return' in expected_answer.keys():
		assert data_response[0].get('name') == expected_answer.get('full_return').get('name')
		assert data_response[0].get('description') == expected_answer.get('full_return').get('description')



@pytest.mark.parametrize(
    ('genre_id', 'expected_status'),
    ES_GENRE_BY_ID_PARAMETRIZE_POSITIVE_DATA + ES_GENRE_BY_ID_PARAMETRIZE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_get_genre_by_id(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    genre_id: Dict[str, Union[str, int, float, None]],
    expected_status: Dict[str, Union[str, int, float, None]]
):

    url = f'{sett.app_api_host}genres/{genre_id.get("genre_id")}'
    response = await make_get_request(url, '')
    data_response = await response.json()

    assert response.status == expected_status.get('status')
    assert len(data_response) == expected_status.get('length')
    if response.status == 404:
        assert data_response.get('detail')[0].get('msg') == expected_status.get('msg')

    if 'full_return' in expected_status.keys():
        assert data_response.get('name') == expected_status.get('full_return').get('name')
        assert data_response.get('description') == expected_status.get('full_return').get('description')
