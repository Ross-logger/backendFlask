from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgres://oomzugrngzshgq:07ddf913052409e8ffb5fe1451a28504244e269ee506ffab18818a6ed513edc9@ec2-54-74-77-126.eu-west-1.compute.amazonaws.com:5432/d6rbu51aggngta'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Session = sessionmaker()
Session.configure(bind=engine)

Base = declarative_base()
