from elasticsearch import AsyncElasticsearch, NotFoundError
from services.queries import (FIND_FILMS_BY_GENRE,
                              FIND_FILMS_BY_QUERY,
                              FIND_FILMS_BY_PERSON,
                              FIND_ALL,
                              FIND_PERSONS_BY_QUERY,
                              FIND_FILMS_BY_PERSONS)


class Common:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    @staticmethod
    def prepare_sorting(sort_param: str):
        if sort_param[0] == '-':
            type_sort = ':desc'
        elif sort_param[0] == '+':
            type_sort = ':asc'
        else:
            type_sort = ':desc'

        return f'{sort_param[1:]}{type_sort}'

    @staticmethod
    def prepare_query(type: str, values: list = None) -> dict:
        if type == 'films_by_genre':
            FIND_FILMS_BY_GENRE['nested']['query']['bool']['must'][0]['match']['genres.id'] = values[0]
            return FIND_FILMS_BY_GENRE
        if type == 'films_by_query':
            FIND_FILMS_BY_QUERY['multi_match']['query'] = values[0]
            return FIND_FILMS_BY_QUERY
        if type == 'films_by_person':
            FIND_FILMS_BY_PERSON['bool']['should'][0]['nested']['query']['bool']['must'][0]['match']['actors.id'] = values[0]
            FIND_FILMS_BY_PERSON['bool']['should'][1]['nested']['query']['bool']['must'][0]['match']['writers.id'] = values[0]
            FIND_FILMS_BY_PERSON['bool']['should'][2]['nested']['query']['bool']['must'][0]['match']['directors.id'] = values[0]
            return FIND_FILMS_BY_PERSON
        if type == 'persons_by_query':
            FIND_PERSONS_BY_QUERY['multi_match']['query'] = values[0]
            return FIND_PERSONS_BY_QUERY
        if type == 'films_by_persons':
            FIND_FILMS_BY_PERSONS['bool']['should'][0]['nested']['query']['terms']['actors.id'] = values
            FIND_FILMS_BY_PERSONS['bool']['should'][1]['nested']['query']['terms']['writers.id'] = values
            FIND_FILMS_BY_PERSONS['bool']['should'][2]['nested']['query']['terms']['directors.id'] = values
            return FIND_FILMS_BY_PERSONS
        if type == 'all':
            return FIND_ALL

    async def _search(self,
                      index: str,
                      query: dict,
                      from_: int = None,
                      size: int = None,
                      sort: str = None
                      ):
        try:
            return await self.elastic.search(
                    index=index,
                    from_=from_,
                    size=size,
                    query=query,
                    sort=sort
                )
        except NotFoundError:
            return None
