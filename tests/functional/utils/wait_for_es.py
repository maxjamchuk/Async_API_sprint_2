# import asyncio
# import time

# from elasticsearch import AsyncElasticsearch


# async def elastic_connect(host: str) -> AsyncElasticsearch:
#     elastic = AsyncElasticsearch(hosts=host)
#     while True:
#         if await elastic.ping():
#             print('HERE')
#             return elastic
#         time.sleep(1)
#         # raise ConnectionError("Connection failed")
#     # return elastic


# async def main():
#     es = await elastic_connect(host=["http://elasticsearch:9200"])
#     await es.close()


# if __name__ == "__main__":
#     asyncio.run(main())

import time

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es_client = Elasticsearch(hosts='http://elasticsearch:9200')
    while True:
        if es_client.ping():
            break
        time.sleep(15)