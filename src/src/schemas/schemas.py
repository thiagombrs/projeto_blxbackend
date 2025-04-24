from pydantic import BaseModel, Field
from typing import Optional, List


class UsuarioSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str

    model_config = {"from_attributes": True}

    class Config:
        orm_mode = True


class LoginData(BaseModel):
    telefone: str
    senha: str


class LoginSucesso(BaseModel):
    usuario: UsuarioSimples
    acess_token: str

    class Config:
        orm_mode = True


class ProdutoSimples(BaseModel):
    id: Optional[int] = None
    nome: str
    preco: float

    class Config:
        orm_mode = True


class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    telefone: str
    senha: str
    produtos: List[ProdutoSimples] = Field(default_factory=list)

    class Config:
        orm_mode = True


class Produto(BaseModel):
    id: Optional[int] = None
    nome: str
    detalhes: Optional[str] = None
    preco: float
    disponivel: bool = True
    usuario_id: Optional[int] = None

    class Config:
        orm_mode = True


class Pedido(BaseModel):
    id: Optional[int] = None
    quantidade: int
    local_entrega: Optional[str] = None
    tipo_entrega: str
    observacao: Optional[str] = Field(default="Sem observações")
    usuario_id: Optional[int] = None
    produto_id: Optional[int] = None
    usuario: Optional[UsuarioSimples] = None
    produto: Optional[ProdutoSimples] = None

    class Config:
        orm_mode = True