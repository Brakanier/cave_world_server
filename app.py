from typing import List
from tortoise.contrib.fastapi import register_tortoise

import models # all db and pydanic models
import services # all services
import config
import websocket

from pydantic import BaseModel
from fastapi import FastAPI, Body, File, UploadFile, Response, Cookie, Request, Depends, Header, HTTPException
from fastapi.responses import RedirectResponse

from fastapi.logger import logger
import logging

from starlette.middleware.cors import CORSMiddleware
from starlette import status
from starlette.routing import WebSocketRoute

import datetime

app = FastAPI()
app.add_websocket_route("/ws/{token}", websocket.EndPoint)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # FIXME for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fh = logging.FileHandler('log.log')

logger.addHandler(fh)

connections = ''#websocket.Connections()
logger.info(f'Object ID - {id(connections)}')


class VkLaunchParams(BaseModel):
    vk_user_id: int
    vk_app_id: int
    vk_is_app_user: bool
    vk_are_notifications_enabled: bool
    vk_language: str
    vk_ref: str
    vk_access_token_settings: str

async def token_auth(x_auth: str = Header(None)):
    if not x_auth:
        raise HTTPException(401, 'Unauthorized')
    return x_auth

game_service = services.Game()
user_service = services.Users()

#vk_user_id: int, vk_app_id: int, vk_is_app_user: bool, vk_are_notifications_enabled: bool, vk_language: str, vk_ref: str, vk_access_token_settings: str
@app.get('/login/vk')
async def login(r: Request, vk_user_id: int):
    vk = services.Vk()
    is_valid = vk.is_valid(r.scope['query_string'])
    if is_valid == False:
        raise HTTPException(401, 'Unauthorized')
    
    
    user = await user_service.get_or_create_vk(vk_user_id)
    return await models.NewUserPydanic.from_tortoise_orm(user)

@app.get('/login/test')
async def login_test(vk_id: str):
    user = await user_service.get_or_create_vk(vk_id)
    return await models.NewUserPydanic.from_tortoise_orm(user)

@app.get('/nickname')
async def set_nickname(nickname: str, token: str = Depends(token_auth)):
    return await user_service.set_nickname(token, nickname)

@app.get('/level-up')
async def level_up(token: str = Depends(token_auth)):
    return await game_service.level_up(token)

@app.get('/data')
async def data(token: str = Depends(token_auth)):
    return await user_service.get_user_data(token)

@app.get('/extract/{target}')
async def extract(target: str, token: str = Depends(token_auth)):
    return await game_service.action(token, target)

@app.get('/build/{target}')
async def build(target: str, token: str = Depends(token_auth)):
    return await game_service.action(token, target)

@app.get('/citizen/{target}/{amount}')
async def citizen(target: str, amount: int, token: str = Depends(token_auth)):
    return await game_service.action(token, target, amount)

@app.get('/find')
async def find_enemies(token: str = Depends(token_auth)):
    return await game_service.find(token)

@app.get('/attack/{enemy_id}')
async def attack(enemy_id: int, token: str = Depends(token_auth)):
    return await game_service.attack(token, enemy_id)

@app.get('/battles')
async def battles(token: str = Depends(token_auth)):
    return await game_service.battles(token)

register_tortoise(
    app,
    db_url=config.DB_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

