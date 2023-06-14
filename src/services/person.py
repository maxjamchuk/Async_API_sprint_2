from functools import lru_cache
from typing import Optional, List, Dict
import uuid

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.film import Films
from models.person import Person
from services.common import Common


class PersonService(Common):
    INDEX = 'persons'

    async def search_by_film_by_person(self,
                                       person_id: uuid.UUID,
                                       page_size: int,
                                       page_number: int
                                       ) -> Optional[List[Films]]:
        try:
            films = await self._search(
                index='movies',
                query=self.prepare_query(type='films_by_person', values=[person_id]),
                from_=page_number,
                size=page_size
            )
        except NotFoundError:
            return None
        return [Films(
                id=row['_source'].get('id'),
                title=row['_source'].get('title'),
                imdb_raiting=row['_source'].get('imdb_raiting')
                ) for row in films['hits']['hits']]

    async def search_persons(self,
                             query: str,
                             page_size: int,
                             page_number: int
                             ) -> Optional[List[Person]]:
        try:
            persons = await self._search(
                index=self.INDEX,
                query=self.prepare_query(type='persons_by_query', values=[query]),
                from_=page_number,
                size=page_size,
                sort='_score'
            )

            person_ids = [row['_source'].get('id') for row in persons["hits"]["hits"]]
            films = await self._search(
                index='movies',
                query=self.prepare_query(type='films_by_persons', values=person_ids),
                from_=page_number,
                size=page_size
            )
            result = []
            for per in persons["hits"]["hits"]:

                per_id = per['_source'].get('id')
                full_name = per['_source'].get('full_name')
                new_films = []
                for fil in films["hits"]["hits"]:
                    roles = []
                    if full_name in fil['_source'].get('director'):
                        roles.append('director')
                    if full_name in fil['_source'].get('actors_names'):
                        roles.append('actor')
                    if full_name in fil['_source'].get('writers_names'):
                        roles.append('writer')

                    if len(roles) == 0:
                        continue
                    new_films.append({'uuid': fil['_source'].get('id'), 'roles': roles})

                result.append(Person(
                    uuid=per_id,
                    full_name=full_name,
                    films=new_films
                ))
            return result

        except NotFoundError:
            return None

    async def get_by_id(self, person_id: uuid.UUID) -> Optional[Person]:
        person = await self._get_person_from_elastic(person_id)
        return person

    async def _get_person_from_elastic(self, person_id: uuid.UUID):
        try:
            doc = await self.elastic.get(index=self.INDEX, id=person_id)
            person_id, full_name = doc['_source'].get('id'), doc['_source'].get('full_name')
        except NotFoundError:
            return None

        films = await self.find_films_roles(person_id=person_id, full_name=full_name)
        return Person(
            uuid=person_id,
            full_name=full_name,
            films=films
        )

    async def find_films_roles(self,
                               person_id: uuid.UUID,
                               full_name: str
                               ) -> Optional[List[Dict[uuid.UUID, List[str]]]]:
        search_films = await self._search(
                index='movies',
                query=self.prepare_query(type='films_by_person', values=[person_id]),
            )
        films = []
        for row in search_films['hits']['hits']:
            roles = []
            if full_name in row['_source'].get('director'):
                roles.append('director')
            if full_name in row['_source'].get('actors_names'):
                roles.append('actor')
            if full_name in row['_source'].get('writers_names'):
                roles.append('writer')

            films.append({'uuid': row['_source'].get('id'), 'roles': roles})
        return films


@lru_cache()
def get_person_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(elastic)
