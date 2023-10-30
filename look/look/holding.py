import falcon
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Veritabanı bağlantısını oluşturun (SQLite kullanılıyor, farklı bir veritabanı türü seçebilirsiniz)
engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

# Kullanıcılar Tablosu
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))
    holding_user_id = Column(Integer, ForeignKey('holding_users.id'))

# Holdingler Tablosu
class Holding(Base):
    __tablename__ = 'holding'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# Holding Çalışanları Tablosu
class HoldingEmployee(Base):
    __tablename__ = 'holding_users'

    id = Column(Integer, primary_key=True)
    holding_id = Column(Integer, ForeignKey('holding.id'))
    name = Column(String)
    last_name = Column(String)

# Şirketler Tablosu
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    holding_id = Column(Integer, ForeignKey('holding.id'))

# Şirket Çalışanları Tablosu
class CompanyEmployee(Base):
    __tablename__ = 'company_users'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    name = Column(String)
    last_name = Column(String)

# Araçlar Tablosu
class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    vehicle_name = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))
    maintenance_date = Column(DateTime)
    maintenance_detail = Column(String)


# Falcon API uygulaması
class UsersResource:
    def on_get(self, req, resp):
        # Kullanıcıları getirme işlemi burada yapılır (SQLAlchemy ile).
        session = Session()
        users = session.query(User).all()
        session.close()
        resp.media = [user.__dict__ for user in users]

class HoldingResource:
    def on_get(self, req, resp):
        # Holding bilgilerini getirme işlemi burada yapılır (SQLAlchemy ile).
        session = Session()
        holdings = session.query(Holding).all()
        session.close()
        resp.media = [holding.__dict__ for holding in holdings]

# Falcon API uygulamasını oluşturun
app = falcon.API()

# API rotalarını tanımlayın
users_resource = UsersResource()
holding_resource = HoldingResource()

app.add_route('/users', users_resource)
app.add_route('/holding', holding_resource)

if __name__ == '__main__':
    httpd = falcon.make_server('127.0.0.1', 8000, app)
    print("Falcon API çalışıyor...")
    httpd.serve_forever()