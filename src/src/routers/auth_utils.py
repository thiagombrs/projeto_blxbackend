from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from fastapi import APIRouter, status, Depends, HTTPException
from src.infra.providers import hash_provider, token_provider
from jose import JWTError
from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/token')

def obter_usuario_logado(token: str =  Depends(oauth2_schema), session: Session = Depends(get_db)):
    try:
        telefone =  token_provider.verificar_access_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token Inválido')
    
    if not telefone:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token Inválido')
    
    usuario = RepositorioUsuario(session).obter_por_telefone(telefone)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token Inválido')
    
    return usuario