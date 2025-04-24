from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models

class RepositorioProduto():

    def __init__(self, db: Session):
        self.session = db

    def criar(self, produto: schemas.Pedido):
        db_produto = models.Pedido(nome=produto.nome,
                                    detalhes=produto.detalhes,
                                    preco=produto.preco,
                                    disponivel=produto.disponivel,
                                    usuario_id=produto.usuario_id)
        
        
        self.session.add(db_produto)
        self.session.commit()
        self.session.refresh(db_produto)
        return db_produto

    def listar(self):
        produtos = self.session.query(models.Pedido).all()
        return produtos
    
    def buscarPorId(self, id: int):
        consulta = select(models.Pedido).where(models.Pedido.id == id)
        produto = self.session.execute(consulta).scalars().first()
        return produto

    def editar(self,  id: int, produto: schemas.Pedido):
        update_stmt = update(models.Pedido).where(models.Pedido.id == id).values(
                                    nome=produto.nome,
                                    detalhes=produto.detalhes,
                                    preco=produto.preco,
                                    disponivel=produto.disponivel
                                    )
        
        self.session.execute(update_stmt)
        self.session.commit()

    def remover(self, id: int):
        delete_stmt = delete(models.Pedido).where(models.Pedido.id == id)

        self.session.execute(delete_stmt)
        self.session.commit()