from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.schemas import Produto, ProdutoSimples
from src.infra.sqlalchemy.repositorios.repositorio_produto import RepositorioProduto
from typing import List
from src.infra.sqlalchemy.config.database import get_db, criar_db

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProdutoSimples)
def criar_produto(produto: Produto, db: Session = Depends(get_db)): 
    produto_criado = RepositorioProduto(db).criar(produto)
    return produto_criado

@router.get('/', response_model=List[ProdutoSimples])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = RepositorioProduto(db).listar()
    return produtos

@router.get('/{id}', response_model=ProdutoSimples)
def exibir_produto(id: int, db: Session = Depends(get_db)):
    produto_localizado = RepositorioProduto(db).buscarPorId(id)
    if not produto_localizado:
        raise HTTPException(status_code=404, detail= f'Não há um produto com o id = {id}')
    return produto_localizado

@router.put('/{id}', response_model=ProdutoSimples)
def atualizar_produto(id: int, produto: Produto, db: Session = Depends(get_db)): 
    produto_atualizado = RepositorioProduto(db).editar(id, produto)
    produto.id = id
    return produto

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(id: int, session: Session = Depends(get_db)):
    RepositorioProduto(session).remover(id)
    return
