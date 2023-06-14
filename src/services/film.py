from functools import lru_cache
from typing import Optional, List
import uuid

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.film import Film, Films
from services.common import Common


class FilmService(Common):
    INDEX = 'movies'

    async def search_by_query(self,
                              query: str,
                              page_size: int,
                              page_number: int
                              ) -> Optional[List[Films]]:
        try:
            films = await self._search(
                index=self.INDEX,
                query=self.prepare_query(type='films_by_query', values=[query]),
                from_=page_number,
                size=page_size,
                sort='_score'
            )
        except NotFoundError:
            return None
        return [Films(
                id=row['_source'].get('id'),
                title=row['_source'].get('title'),
                imdb_raiting=row['_source'].get('imdb_raiting')
                ) for row in films["hits"]["hits"]]

    async def get_all(self,
                      genre: uuid.UUID,
                      sort_param: str,                      
                      page_size: int,
                      page_number: int
                      ) -> Optional[List[Films]]:
        films = await self._get_films_from_elastic(
            sort_param=sort_param,
            page_size=page_size,
            page_number=page_number,
            genre=genre
        )
        if not films:
            return None
        return films

    async def _get_films_from_elastic(self,
                                      genre: uuid.UUID,
                                      sort_param: str,
                                      page_size: int,
                                      page_number: int
                                      ) -> Optional[List[Films]]:
        try:
            sorting = self.prepare_sorting(sort_param=sort_param)
            if genre:
                query = self.prepare_query(type='films_by_genre', values=[genre])
            else:
                query = self.prepare_query(type='all')

            result = await self._search(
                index=self.INDEX,
                from_=page_number,
                size=page_size,
                query=query,
                sort=sorting
            )
        except NotFoundError:
            return None
        return [Films(
                id=row['_source'].get('id'),
                title=row['_source'].get('title'),
                imdb_raiting=row['_source'].get('imdb_raiting')
                ) for row in result["hits"]["hits"]]

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: uuid.UUID) -> Optional[Film]:
        film = await self._get_film_from_elastic(film_id)
        return film

    async def _get_film_from_elastic(self, film_id: uuid.UUID) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index=self.INDEX, id=film_id)
        except NotFoundError:
            return None

        return Film(
            id=doc['_source'].get('id'),
            title=doc['_source'].get('title'),
            description=doc['_source'].get('description'),
            imdb_raiting=doc['_source'].get('imdb_raiting'),
            genres=doc['_source'].get('genres'),
            actors=doc['_source'].get('actors'),
            writers=doc['_source'].get('writers'),
            directors=doc['_source'].get('directors')
        )


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    return FilmService(elastic)
