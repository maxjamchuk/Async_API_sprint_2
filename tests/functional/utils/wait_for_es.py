import asyncio

from elasticsearch import AsyncElasticsearch


async def elastic_connect(host: str) -> AsyncElasticsearch:
    elastic = AsyncElasticsearch(hosts=host)
    if not await elastic.ping():
        raise ConnectionError("Connection failed")
    return elastic


async def main():
    es = await elastic_connect(host=["http://elasticsearch:9200"])
    await es.close()


if __name__ == "__main__":
    asyncio.run(main())
