from DatabaseService.DeclarativeBase import Base as Model
from sqlalchemy import Column, Integer, ForeignKey, Text, Float
from sqlalchemy.orm import relationship


class EquivalencesModel(Model):
    __tablename__ = 'equivalences'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit_1_id = Column(Integer, ForeignKey('units.id'))
    unit_2_id = Column(Integer, ForeignKey('units.id'))
    multiplier = Column(Float, nullable=False)
    unit_1 = relationship('Units', foreign_keys=[unit_1_id])
    unit_2 = relationship('Units', foreign_keys=[unit_2_id])