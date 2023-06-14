import os

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv("ELASTIC_HOST", "127.0.0.1")
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", 9200))
ELASTIC_SCHEME = os.getenv("ELASTIC_SCHEME", "http")
