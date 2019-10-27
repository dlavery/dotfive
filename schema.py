from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    parent_id = Column(Integer, ForeignKey('category.id'))
    children = relationship("Category", cascade="all, delete, delete-orphan")
    items = relationship("Item", back_populates="category", cascade="all, delete, delete-orphan")

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    label = Column(String(50))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="items")

def main(dbname):
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///'+dbname, echo=True)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dbname', help='The database name')
    args = parser.parse_args()
    main(args.dbname)
