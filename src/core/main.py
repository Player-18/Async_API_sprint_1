import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, orjson
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import films
from core import config
from db import redis, elastic

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event('startup')
# async def startup():
#     # Подключаемся к базам при старте сервера
#     # Подключиться можем при работающем event-loop
#     # Поэтому логика подключения происходит в асинхронной функции
#     redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
#     elastic.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_SCHEMA}{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
#
#
# @app.on_event('shutdown')
# async def shutdown():
#     # Отключаемся от баз при выключении сервера
#     await redis.redis.close()
#     await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
