from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db, criar_db
from typing import List
from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario
from src.schemas.schemas import Usuario, UsuarioSimples, LoginData, LoginSucesso
from src.infra.providers import hash_provider, token_provider
from src.routers.auth_utils import obter_usuario_logado

router = APIRouter()


@router.post("/signup")
def signup(usuario: Usuario, db: Session = Depends(get_db)):  # <- aqui está o segredo
    usuario_localizado = RepositorioUsuario(db).obter_por_telefone(usuario.telefone)
    
    if usuario_localizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Telefone já cadastrado")
    
    usuario.senha = hash_provider.gerar_hash(usuario.senha)

    usuario_criado = RepositorioUsuario(db).criar(usuario)
    return usuario_criado

@router.get("/usuarios", response_description=List[Usuario])
def listar_usuario(session: Session = Depends(get_db)):
    usuarios = RepositorioUsuario(session).listar()
    return usuarios

@router.post("/token", response_model=LoginSucesso)
def login(login_data: LoginData, session: Session = Depends(get_db)):
    senha = login_data.senha
    telefone = login_data.telefone

    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Telefone ou não senha incorretos')
    
    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)

    if not senha_valida:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Telefone ou não senha incorretos')
    
    token = token_provider.criar_access_token({"sub": usuario.telefone})
    return LoginSucesso(usuario=usuario, acess_token=token)


@router.get('/me', response_model=UsuarioSimples)
def me(usuario: Usuario = Depends(obter_usuario_logado)):
    return usuario
