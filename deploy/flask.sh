#!/bin/bash

set -e
set -x

gzip -cd "/tmp/flask-training-api.gz" | docker load

docker stop flask-training-api-{$FLAVOR} || true
sleep 10
docker kill flask-training-api-{$FLAVOR} || true

set +x
echo "running docker run [hidden secrets]"

docker run -d --rm -p 0.0.0.0:{$PORT}:8080 \
	-e FLASK_SENTRY_CONFIG__environment="{$FLAVOR}" \
	--name flask-training-api-{$FLAVOR} flask-training-api:latest
