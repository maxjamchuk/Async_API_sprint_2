import uuid

ES_PERSON_SEARCH_PARAMETRIZE_POSITIVE_DATA = [
    (
        'person',
        {'query': 'Ann', 'page_number': 0, 'page_size': 50},
        {'status': 200, 'length': 1}
    ),
    (
        'person',
        {'query': 'Ann', 'page_number': 0, 'page_size': 2},
        {'status': 200, 'length': 1}
    ),
    (
        'person',
        {'query': 'Ann'},
        {'status': 200, 'length': 1}
    ),
    (
        'person',
        {'query': 'Ann', 'page_number': 0, 'page_size': 1},
        {'status': 200, 'length': 1, 'full_return': [
            {
                "id": uuid.UUID('c0b89c7f-01ef-49aa-854f-b48676b36885'),
                "full_name": "Ann"
            }
        ]}
    )
]

ES_PERSON_SEARCH_PARAMETRIZE_NEGATIVE_DATA = [
    (
        'person',
        {'query': 'Musseti', 'page_number': 0, 'page_size': 50},
        {'status': 404, 'length': 1}
    ),
    (
        'person',
        {'query': 'Musseti', 'page_number': -1, 'page_size': 50},
        {'status': 422, 'length': 1, 'msg': 'ensure this value is greater than or equal to 0'}
    ),
    (
        'person',
        {'query': 'Musseti', 'page_size': 1000000},
        {'status': 422, 'length': 1, 'msg': 'ensure this value is less than or equal to 500'}
    )
]

ES_PERSON_SEARCH_GEN_DATA = [
    {
        'id': uuid.UUID('c0b89c7f-01ef-49aa-854f-b48676b36885'),
        'full_name': 'Ann',
    },
    {
        'id': uuid.UUID('d5fb741d-93a9-4ced-b788-e162e8567256'),
        'full_name': 'Bob',
    },
    {
        'id': uuid.UUID('407452e9-5709-4597-acc6-e2daa3c5255d'),
        'full_name': 'Ben',
    },
    {
        'id': uuid.UUID('93e34623-4522-41c0-83a4-a7f697671242'),
        'full_name': 'Howard',
    },
    {
        'id': uuid.UUID('93b712a6-d5ae-492e-8462-3512014cbf2c'),
        'full_name': 'Stan',
    },
]