from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///holding.db', echo = True)

Base = declarative_base()

# Kullanıcılar Tablosu
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    companies = relationship("Company", back_populates="c_user")
    holding = relationship("Holding", back_populates="h_user")

# Şirketler Tablosu
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="companies")
    vehicles = relationship("Vehicle", back_populates="company")

# Holding Tablosu
class Holding(Base):
    __tablename__ = 'holding'

    id = Column(Integer, primary_key=True)
    holding_name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    user = relationship("User", back_populates="companies")
    vehicles = relationship("Vehicle", back_populates="company")

# Araçlar Tablosu
class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    vehicle_name = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))
    holding_id = Column(Integer, ForeignKey('companies.id'))
    maintenance_date = Column(DateTime)
    maintenance_detail = Column(String)

    company = relationship("Company", back_populates="c_vehicles")
    holding = relationship("Holding", back_populates="h_vehicles")






