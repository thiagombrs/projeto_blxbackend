from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = '698dc19d489c4e4db73e28a713eab07b'
ALGORITHN = 'HS256'
EXPIRES_IN_MIN = 3000


def criar_access_token(data: dict):
    dados = data.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MIN)

    dados.update({'exp': expiracao})

    token_jwt = jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHN)
    return token_jwt


def verificar_access_token(token: str):

    carga = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHN])
    return carga.get('sub')