from pydantic import BaseModel
from typing import Optional, List

class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float
    disponivel: bool

    class config:
        orm_mode = True

class LoginData(BaseModel):
    senha: str
    telefone: str


class UsuarioSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str

    model_config = {
        "from_attributes": True  # Permite converter de ORM automaticamente
    }
    
    class config:
        orm_mode = True

class LoginSucesso(BaseModel):
    usuario: UsuarioSimples
    acess_token: str

class Pedido(BaseModel):
    id: Optional[int] = None
    nome: str
    detalhes: str
    preco: float
    disponivel: bool = False
    usuario_id: Optional[int] = None
    usuario: Optional[UsuarioSimples] = None

    class config:
        orm_mode = True

class ProdutoSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float

    class config:
        orm_mode = True

class Pedido(BaseModel):
    id: Optional[int] = None
    quantidade: int
    local_entrega: Optional[str] = None
    tipo_entrega: str
    observacao: Optional[str] = 'Sem observações'

    usuario_id: Optional[int] = None
    produto_id: Optional[int] = None

    usuario: Optional[UsuarioSimples] = []
    produto: Optional[ProdutoSimples] = []

    class config:
        orm_mode = True

class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str
    senha: str
    produtos: List[ProdutoSimples] = []
    
    class config:
        orm_mode = True
