import os
import unittest
import argparse
import schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def test_01_add_category(self):
        session = Session()
        try:
            category = schema.Category(name='Electronics')
            session.add(category)
            session.commit()
        except Exception as e:
            session.rollback()
            raise(e)
        self.assertEqual(category.id, 1)

    def test_02_add_2nd_category(self):
        session = Session()
        try:
            category = schema.Category(name='Gaming consoles')
            session.add(category)
            session.commit()
        except Exception as e:
            session.rollback()
            raise(e)
        self.assertEqual(category.id, 2)

    def test_03_add_child_category(self):
        session = Session()
        try:
            parent = session.query(schema.Category).filter_by(name='Electronics').first()
            category = schema.Category(name='Televisions', parent_id=parent.id)
            session.add(category)
            session.commit()
        except Exception as e:
            session.rollback()
            raise(e)
        self.assertEqual(parent.children[0].id, 3)

    def test_04_add_tv_item(self):
        session = Session()
        try:
            category = session.query(schema.Category).filter_by(name='Televisions').first()
            item = schema.Item(label='49-inch LCD', category_id=category.id)
            session.add(item)
            session.commit()
        except Exception as e:
            session.rollback()
            raise(e)
        self.assertEqual(item.id, 1)
        self.assertEqual(category.items[0].id, 1)

    def test_05_add_console_item(self):
        session = Session()
        try:
            category = session.query(schema.Category).filter_by(name='Gaming consoles').first()
            item = schema.Item(label='PS4 Pro', category_id=category.id)
            session.add(item)
            session.commit()
        except Exception as e:
            session.rollback()
            raise(e)
        self.assertEqual(item.id, 2)
        self.assertEqual(category.items[0].id, 2)

    def test_06_cascade_delete_console(self):
        session = Session()
        try:
            category = session.query(schema.Category).filter_by(name='Gaming consoles').first()
            session.delete(category)
            session.commit()
            categories = session.query(schema.Category).filter_by(name='Gaming consoles').count()
            self.assertEqual(categories, 0)
            items = session.query(schema.Item).filter_by(label='PS4 Pro').count()
            self.assertEqual(items, 0)
        except Exception as e:
            session.rollback()
            raise(e)

    def test_07_cascade_delete_electronics(self):
        session = Session()
        try:
            category = session.query(schema.Category).filter_by(name='Electronics').first()
            session.delete(category)
            session.commit()
            categories = session.query(schema.Category).count()
            self.assertEqual(categories, 0)
            items = session.query(schema.Item).count()
            self.assertEqual(items, 0)
        except Exception as e:
            session.rollback()
            raise(e)

if __name__ == '__main__':
    dbname = "dbtest"
    os.remove(dbname)
    schema.main(dbname)
    engine = create_engine("sqlite:///"+dbname, echo=False)
    Session = sessionmaker(bind=engine)
    unittest.main()
