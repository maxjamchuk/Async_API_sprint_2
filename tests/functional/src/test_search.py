import uuid
import pytest

from typing import Coroutine, Dict, Union

from ..settings import test_settings as sett
from ..testdata.film import (
    UUIDS_FILMS,
    ES_FILM_SEARCH_GEN_DATA,
    ES_FILM_SEARCH_PARAMETRIZE_POSITIVE_DATA,
    ES_FILM_SEARCH_PARAMETRIZE_NEGATIVE_DATA,
)
from ..testdata.person import (
    ES_PERSON_SEARCH_GEN_DATA,
    ES_PERSON_SEARCH_PARAMETRIZE_POSITIVE_DATA,
    ES_PERSON_SEARCH_PARAMETRIZE_NEGATIVE_DATA
)


@pytest.mark.parametrize(
    'test_type, query_data, expected_answer',
    ES_FILM_SEARCH_PARAMETRIZE_POSITIVE_DATA \
    + ES_FILM_SEARCH_PARAMETRIZE_NEGATIVE_DATA \
    + ES_PERSON_SEARCH_PARAMETRIZE_POSITIVE_DATA \
    + ES_PERSON_SEARCH_PARAMETRIZE_NEGATIVE_DATA
)
@pytest.mark.anyio
async def test_search(
    make_get_request: Coroutine,
    es_write_data: Coroutine,
    test_type: str,
    query_data: Dict[str, Union[str, int, float, None]],
    expected_answer: Dict[str, Union[str, int, float, None]],
):
    
    # prepare data to request
    if test_type == 'film':
        url = f'{sett.app_api_host}films/search'
    elif test_type == 'person':
        url = f'{sett.app_api_host}persons/search'
    else:
        assert 1 == 0
    
    # load data into es
    es_data = []
    for film_id in UUIDS_FILMS:
        ES_FILM_SEARCH_GEN_DATA['id'] = film_id
        es_data.append(ES_FILM_SEARCH_GEN_DATA.copy())

    await es_write_data(data=es_data, index='movies')
    await es_write_data(data=ES_PERSON_SEARCH_GEN_DATA, index='persons')
    
    # make a request
    response = await make_get_request(url, params=query_data)
    data_response = await response.json()
    
    # check tests
    assert response.status == expected_answer.get('status')
    assert len(data_response) == expected_answer.get('length')
    if response.status == 422:
        assert data_response.get('detail')[0].get('msg') == expected_answer.get('msg')

    if 'full_return' in expected_answer.keys():
        if test_type == 'film':
            assert data_response[0].get('title') == expected_answer.get('full_return')[0].get('title')
            assert data_response[0].get('imdb_raiting') == expected_answer.get('full_return')[0].get('imdb_raiting')
        if test_type == 'person':
            assert uuid.UUID(data_response[0].get('uuid')) == expected_answer.get('full_return')[0].get('id')
            assert data_response[0].get('full_name') == expected_answer.get('full_return')[0].get('full_name')
