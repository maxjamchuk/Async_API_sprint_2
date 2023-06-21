import uuid
import pytest

from typing import Coroutine, Dict, Union

from ..settings import test_settings as sett
from ..testdata.genre import ES_GENRE_GEN_DATA
from ..testdata.film import UUIDS_FILMS, ES_FILM_SEARCH_GEN_DATA


@pytest.mark.anyio
async def test_get_all_genres(
	make_get_request: Coroutine,
	es_write_data: Coroutine,
):
	# Load data into ES
	await es_write_data(data=ES_GENRE_GEN_DATA, index='genres')

	# Make a request
	url = f'{sett.app_api_host}genres'
	response = await make_get_request(url, params={})
	data_response = await response.json()

	# Check tests
	assert response.status == 200
	assert len(data_response) == len(ES_GENRE_GEN_DATA)
	for i, genre in enumerate(data_response):
		assert genre['id'].lower() == str(ES_GENRE_GEN_DATA[i]['id']).lower()
		assert genre['name'] == ES_GENRE_GEN_DATA[i]['name']


@pytest.mark.parametrize(
	'genre_id, expected_status',
	[
		(str(genre['id']), 200) for genre in ES_GENRE_GEN_DATA
	]
)
@pytest.mark.anyio
async def test_get_genre_by_id(
	make_get_request: Coroutine,
	es_write_data: Coroutine,
	genre_id: str,
	expected_status: int,
):
	# Load data into ES
	await es_write_data(data=ES_GENRE_GEN_DATA, index='genres')

	# Make a request
	url = f'{sett.app_api_host}genres/{genre_id}'
	response = await make_get_request(url, params={})

	# Check tests
	assert response.status == expected_status
