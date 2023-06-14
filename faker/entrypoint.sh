#!/bin/sh

while ! curl elasticsearch:$ELASTIC_PORT; do
    sleep 10
done

# need to wait when elastic create indexes.
sleep 30
python faker/main.py

exec "$@"