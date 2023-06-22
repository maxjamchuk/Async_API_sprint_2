import uuid


ES_GENRE_GEN_DATA = [
    {
        "id" : uuid.UUID('0fbcd2b3-2792-4468-8885-06d653f368c8'),
        "name" : "Action",
        "description" : "Answer pick always. Organization nice force middle result well brother ask. Evening use agreement av... Behind blood by evidence learn parent accept."
    },
    {
        "id" : uuid.UUID('b29306f4-e843-4f6f-96c8-0e815a504575'),
        "name" : "Sci-Fi",
        "description" : "Answer pick always. Organization nice force middle result well brother ask. Evening use agreement av... Behind blood by evidence learn parent accept."
    },
]


ES_GENRES_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'page_number': 0, 'page_size': 50},
        {'status': 200, 'length': 2}
    ),
    (
        {'page_number': 1, 'page_size': 50},
        {'status': 200, 'length': 1}
    ),
]

ES_GENRES_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'genre': 'nonexistent_genre_id', 'page_number': 0, 'page_size': 50},
        {'status': 200, 'length': 2, 'msg': 'Genre not found'}
    ),
    (
        {'genre': '0cc0ee04-e27c-4c5a-a157-a408e799b651', 'page_number': -1, 'page_size': 50},
        {'status': 422, 'length': 1, 'msg': 'ensure this value is greater than or equal to 0'}
    ),
    (
        {'genre': '0cc0ee04-e27c-4c5a-a157-a408e799b651', 'page_size': 1000000},
        {'status': 422, 'length': 1, 'msg': 'ensure this value is less than or equal to 500'}
    )
]


ES_GENRE_BY_ID_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'genre_id': '0fbcd2b3-2792-4468-8885-06d653f368c8'},
        {'status': 200, 'length': 3, 'full_return' : {
                "id": "1",
                "name": "Action",
                "description": "Answer pick always. Organization nice force middle result well brother ask. Evening use agreement av... Behind blood by evidence learn parent accept."
            }
        }
    ),
    (
        {'genre_id': 'b29306f4-e843-4f6f-96c8-0e815a504575'},
        {'status': 200, 'length': 3, 'full_return' : {
                "id": "1",
                "name": "Sci-Fi",
                "description": "Answer pick always. Organization nice force middle result well brother ask. Evening use agreement av... Behind blood by evidence learn parent accept."
            }
        }
    )
]


ES_GENRE_BY_ID_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'genre_id': '123'},
        {'status': 404, 'length': 1, 'msg': 'Genre not found'}
    ),
    (
        {'genre_id': 123},
        {'status': 404, 'length': 1, 'msg': 'Genre not found'}
    )
]
