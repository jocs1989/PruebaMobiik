#!/usr/bin/env bash
docker compose --env-file .env.dev up --build -d   
# Colores
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
YELLOW="\033[1;33m"
MAGENTA="\033[0;35m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${CYAN}🐳 Docker containers activos:${RESET}\n"

docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" \
| sed "s/fastapi-app/${GREEN}&${RESET}/" \
| sed "s/ollama/${MAGENTA}&${RESET}/" \
| sed "s/pgadmin/${BLUE}&${RESET}/" \
| sed "s/mongo-express/${YELLOW}&${RESET}/" \
| sed "s/redisinsight/${RED}&${RESET}/" \
| sed "s/postgres/${CYAN}&${RESET}/" \
| sed "s/redis/${RED}&${RESET}/" \
| sed "s/mongo/${YELLOW}&${RESET}/"

echo -e "\n${CYAN}🔗 URLs disponibles:${RESET}\n"

echo -e "${GREEN}FastAPI:${RESET}        http://0.0.0.0:8080/api/v1/docs"
echo -e "${MAGENTA}Ollama API:${RESET}     http://0.0.0.0:11434"
echo -e "${BLUE}pgAdmin:${RESET}        http://0.0.0.0:5050"
echo -e "${YELLOW}Mongo Express:${RESET} http://0.0.0.0:8081"
echo -e "${RED}Redis Insight:${RESET} http://0.0.0.0:5540"

echo -e "\n${CYAN}📦 Bases de datos:${RESET}"
echo -e "Postgres: localhost:5432"
echo -e "MongoDB:  localhost:27017"
echo -e "Redis:    localhost:6379\n"