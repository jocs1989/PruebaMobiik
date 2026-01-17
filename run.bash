#!/usr/bin/env bash
docker compose --env-file .env.dev up --build -d 
docker ps