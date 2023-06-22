import uuid


UUIDS_GENRES = [
    uuid.UUID("0ce50db6-6c9f-4ffb-99d7-089497bc0a45"),
    uuid.UUID("689b4bc0-e9c6-44aa-b14a-0eb7f91346ba"),
    uuid.UUID("0ef7ba62-a99b-4c19-be18-3c09fd757362"),
    uuid.UUID("a373648f-c455-4386-a63b-dd93afea14d5"),
    uuid.UUID("b600c425-71e6-419e-8a45-e027cc65181a")

]

ES_GENRE_GEN_DATA = [
    {
        "id" : uuid.UUID('0fbcd2b3-2792-4468-8885-06d653f368c8'),
        "name" : "yeah",
        "description" : "Answer pick always. Organization nice force middle result well brother ask. Evening use agreement av... Behind blood by evidence learn parent accept."
    },
    {
        "id" : uuid.UUID('b29306f4-e843-4f6f-96c8-0e815a504575'),
        "name" : "them",
        "description" : "Answer pick always. Organization nice force middle result well brother ask. Evening use agreement av... Behind blood by evidence learn parent accept."
    },

]


ES_GENRES_PARAMETRIZE_POSITIVE_DATA = [
    (
        {'page_number': 0, 'page_size': 50},
        {'status': 200, 'length': 50}
    ),
    (
        {'page_number': 1, 'page_size': 50},
        {'status': 200, 'length': 50}
    ),
]

ES_GENRES_PARAMETRIZE_NEGATIVE_DATA = [
    (
        {'genre': 'nonexistent_genre_id', 'page_number': 0, 'page_size': 50},
        {'status': 422, 'length': 1, 'msg': 'Genre not found'}
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
        {'genre_id': 'a373648f-c455-4386-a63b-dd93afea14d5'},
        {'status': 200, 'length': 3, 'full_return' : {
                "id": "1",
                "name": "yeah",
                "description": "Side ask need. Administration ok light agreement note end positive. Particular Congress letter fast she."
            }
        }
    ),
    (
        {'genre_id': 'b600c425-71e6-419e-8a45-e027cc65181a'},
        {'status': 200, 'length': 3, 'full_return' : {
                "id": "1",
                "name": "them",
                "description": "Short success teacher sometimes provide. Born can impact shake later agree teach. Clear question city official attack. Attack prepare mind imagine a."
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
