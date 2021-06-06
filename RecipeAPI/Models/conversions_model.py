from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Float


class ConversionsModel(Model):
    __tablename__ = 'equivalences'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit_1_id = Column(Integer, ForeignKey('units.id'))
    unit_2_id = Column(Integer, ForeignKey('units.id'))
    factor = Column(Float, nullable=False)