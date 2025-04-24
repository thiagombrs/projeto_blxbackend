from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.schemas import Pedido, ProdutoSimples
from src.infra.sqlalchemy.repositorios.repositorio_produto import RepositorioProduto
from typing import List
from src.infra.sqlalchemy.config.database import get_db, criar_db

router = APIRouter()

@router.post('/produtos', status_code=status.HTTP_201_CREATED, response_model=Pedido)
def criar_produto(produto: Pedido, db: Session = Depends(get_db)): 
    produto_criado = RepositorioProduto(db).criar(produto)
    return produto_criado

@router.get('/produtos', response_model=List[ProdutoSimples])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = RepositorioProduto(db).listar()
    return produtos

@router.get('/produtos/{id}')
def exibir_produto(id: int, db: Session = Depends(get_db)):
    produto_localizado = RepositorioProduto(db).buscarPorId(id)
    if not produto_localizado:
        raise HTTPException(status_code=404, detail= f'Não há um produto com o id = {id}')
    return produto_localizado

@router.put('/produtos/{id}', response_model=ProdutoSimples)
def atualizar_produto(id: int, produto: Pedido, db: Session = Depends(get_db)): 
    produto_atualizado = RepositorioProduto(db).editar(id, produto)
    produto.id = id
    return produto

@router.delete('/produtos/{id}')
def remover_produto(id: int, session: Session = Depends(get_db)):
    RepositorioProduto(session).remover(id)
    return
