from functools import lru_cache
from typing import Optional, List

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.film import Genres
from services.common import Common


class GenreService(Common):
    INDEX = 'genres'

    async def search_by_query(
        self,
        query: str,
        page_size: int,
        page_number: int,
    ) -> Optional[List[Genres]]:
        try:
            result = await self._search(
                index=self.INDEX,
                query=self.prepare_query(type='genres_by_query', values=[query]),
                from_=page_number,
                size=page_size,
                sort='_score',
            )
        except NotFoundError:
            return None

        return [
            Genres(
                id=row['_source'].get('id'),
                name=row['_source'].get('name'),
                description=row['_source'].get('description'),
            )
            for row in result['hits']['hits']
        ]

    async def get_all(
        self,
        page_size: int,
        page_number: int,
    ) -> Optional[List[Genres]]:
        try:
            result = await self._search(
                index=self.INDEX,
                query=self.prepare_query(type='all'),
                from_=page_number,
                size=page_size,
            )
        except NotFoundError:
            return None

        return [
            Genres(
                **row['_source'],
            )
            for row in result['hits']['hits']
        ]

    async def get_by_id(self, genre_id: str) -> Optional[Genres]:
        genre = await self._get_genre_from_elastic(genre_id)
        if not genre:
            return None

        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genres]:
        try:
            doc = await self.elastic.get(index=self.INDEX, id=genre_id)
        except NotFoundError:
            return None

        return Genres(**doc['_source'])


@lru_cache()
def get_genre_service(
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(elastic)
