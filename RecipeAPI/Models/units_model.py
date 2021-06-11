from database_service.base import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


class UnitsModel(Model):
    __tablename__ = 'units'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit = Column(Text, unique=True)
    type = Column(Text, nullable=False)
    number = Column(Text, nullable=False)

    conversion = relationship(
        'ConversionsModel',
        primaryjoin="(or_(UnitsModel.id == ConversionsModel.unit_1_id, UnitsModel.id == ConversionsModel.unit_2_id))")