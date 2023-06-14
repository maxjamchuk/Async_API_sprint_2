#!/bin/sh

while ! curl elasticsearch:$ELASTIC_PORT; do
    sleep 10
done

sleep 5
curl -XPUT http://elasticsearch:$ELASTIC_PORT/movies -H 'Content-Type: application/json' -d @index_movies.json
sleep 5
curl -XPUT http://elasticsearch:$ELASTIC_PORT/genres -H 'Content-Type: application/json' -d @index_genres.json
sleep 5
curl -XPUT http://elasticsearch:$ELASTIC_PORT/persons -H 'Content-Type: application/json' -d @index_persons.json
sleep 5

elasticdump --input=dump_movies.json --output=http://elasticsearch:$ELASTIC_PORT/movies --type=data
elasticdump --input=dump_genres.json --output=http://elasticsearch:$ELASTIC_PORT/genres --type=data
elasticdump --input=dump_persons.json --output=http://elasticsearch:$ELASTIC_PORT/persons --type=data

exec "$@"