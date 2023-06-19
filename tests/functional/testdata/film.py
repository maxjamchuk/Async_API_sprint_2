import uuid

ES_FILM_SEARCH_PARAMETRIZE_POSITIVE_DATA = [
    (
        'film',
        {'query': 'The Star', 'page_number': 0, 'page_size': 50},
        {'status': 200, 'length': 50}
    ),
    (
        'film',
        {'query': 'The Star', 'page_number': 1, 'page_size': 2},
        {'status': 200, 'length': 2}
    ),
    (
        'film',
        {'query': 'The Star'},
        {'status': 200, 'length': 50}
    ),
    (
        'film',
        {'query': 'The Star', 'page_number': 0, 'page_size': 1},
        {'status': 200, 'length': 1, 'full_return': [
            {
                "id": "1",
                "title": "The Star",
                "imdb_raiting": 8.5
            }
        ]}
    )
]

ES_FILM_SEARCH_PARAMETRIZE_NEGATIVE_DATA = [
    (
        'film',
        {'query': 'Mashed potato', 'page_number': 0, 'page_size': 50},
        {'status': 404, 'length': 1}
    ),
    (
        'film',
        {'query': 'Mashed potato', 'page_number': -1, 'page_size': 50},
        {'status': 422, 'length': 1, 'msg': 'ensure this value is greater than or equal to 0'}
    ),
    (
        'film',
        {'query': 'Mashed potato', 'page_size': 1000000},
        {'status': 422, 'length': 1, 'msg': 'ensure this value is less than or equal to 500'}
    )
]

ES_FILM_SEARCH_GEN_DATA = {
        'id': '',
        'imdb_raiting': 8.5,
        'genres': [
            {'id': '000', 'name': 'Action'},
            {'id': '001', 'name': 'Sci-Fi'}
        ],
        'genre': ['Action', 'Sci-Fi'],
        'title': 'The Star',
        'description': 'New World',
        'director': ['Stan'],
        'actors_names': ['Roger'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': uuid.UUID('c0b89c7f-01ef-49aa-854f-b48676b36885'), 'name': 'Ann'},
            {'id': uuid.UUID('d5fb741d-93a9-4ced-b788-e162e8567256'), 'name': 'Bob'}
        ],
        'writers': [
            {'id': uuid.UUID('407452e9-5709-4597-acc6-e2daa3c5255d'), 'name': 'Ben'},
            {'id': uuid.UUID('93e34623-4522-41c0-83a4-a7f697671242'), 'name': 'Howard'}
        ],
        'directors': [
            {'id': uuid.UUID('93b712a6-d5ae-492e-8462-3512014cbf2c'), 'name': 'Stan'},
        ],
    }