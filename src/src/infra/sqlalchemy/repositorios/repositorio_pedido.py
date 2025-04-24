from sqlalchemy import update, delete, select
from sqlalchemy.orm import Session
from typing import List
from src.schemas import schemas
from src.infra.sqlalchemy.models import models


class RepositorioPedido():

    def __init__(self, db: Session):
        self.session = db

    def gravar_pedido(self, pedido: schemas.Pedido):
        db_pedido = models.Pedido(
                                    quantidade=pedido.quantidade,
                                    local_entrega=pedido.local_entrega,
                                    tipo_entrega=pedido.tipo_entrega,
                                    observacao=pedido.observacao,
                                    usuario_id=pedido.usuario_id,
                                    produto_id=pedido.produto_id
                                    )
        
        
        self.session.add(db_pedido)
        self.session.commit()
        self.session.refresh(db_pedido)
        return db_pedido
    

    def buscar(self):
        pedidos = self.session.query(models.models.Pedido).all()
        return pedidos
    
    def buscar_por_id(self, id: int):
        consulta = select(models.Pedido).where(models.Pedido.id == id)
        pedido = self.session.execute(consulta).scalars().first()
        return pedido

    def listar_meus_pedidos_por_uduario_id(self, usuario_id: int):
        consulta = select(models.Pedido).where(models.Pedido.usuario_id == usuario_id)
        pedido = self.session.execute(consulta).scalars().all()
        return pedido
    
    def listar_meus_vendas_por_uduario_id(self, usuario_id: int):
        consulta = select(models.Pedido).join_from(models.Pedido, models.Produto).where(models.Pedido.usuario_id == usuario_id)
        pedido = self.session.execute(consulta).scalars().all()
        return pedido
    
    def editar(self,  id: int, pedido: schemas.Pedido) -> List[models.Pedido]:
        update_stmt = update(models.Pedido).where(models.Pedido.id == id).values(
                                    quantidade=pedido.quantidade,
                                    local_entrega=pedido.local_entrega,
                                    tipo_entrega=pedido.tipo_entrega,
                                    observacao=pedido.observacao
                                    )
        
        self.session.execute(update_stmt)
        self.session.commit()

    def remover(self, id: int):
        delete_stmt = delete(models.Pedido).where(models.Pedido.id == id)

        self.session.execute(delete_stmt)
        self.session.commit()