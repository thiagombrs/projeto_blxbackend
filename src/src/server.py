from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.routers import rotas_produtos
from src.routers import rotas_auth
from src.routers import rotas_pedidos


#criar_db()

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Rotas PRODUTOS
app.include_router(rotas_produtos.router)
app.include_router(rotas_auth.router, prefix="/auth")
app.include_router(rotas_pedidos.router)

