from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositorio_pedido import RepositorioPedido
from src.schemas.schemas import Pedido, Usuario
from src.routers.auth_utils import obter_usuario_logado

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Pedido)
def fazer_pedido(pedido: Pedido, session: Session = Depends(get_db)):
    pedido_criado = RepositorioPedido(session).gravar_pedido(pedido)
    return pedido_criado


@router.get('/{id}', response_model=Pedido)
def exibir_pedido(id: int, session: Session = Depends(get_db)):
    try:
        pedido = RepositorioPedido(session).buscar_por_id(id)
        return pedido
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um pedido com o id: {id}")

@router.get('/auth', response_model=List[Pedido])
def listar_pedido(usuario: Usuario = Depends(obter_usuario_logado), session: Session = Depends(get_db)):
    pedidos = RepositorioPedido(session).listar_meus_pedidos_por_uduario_id(usuario.id)
    return pedidos

@router.get('/{usuario_id}/vendas', response_model=List[Pedido])
def listar_vendas(usuario_id: int, session: Session = Depends(get_db)):
    pedidos = RepositorioPedido(session).listar_meus_vendas_por_uduario_id(usuario_id)
    return pedidos