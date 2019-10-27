import os
import unittest
import argparse
import schema
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestAPI(unittest.TestCase):

    def setUp(self):
        pass

    def test_01_get_categories(self):
        r = requests.get('http://localhost:5000/categories')
        data = r.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['text'], 'Electronics')

    def test_02_create_category(self):
        r = requests.post('http://localhost:5000/category', json={'parent': '', 'name': 'api test 02'})
        self.assertEqual(r.status_code, 200)
        session = Session()
        q = session.query(schema.Category).filter_by(name='api test 02')
        session.close()
        self.assertNotEqual(q, None)

    def test_03_create_subcategory(self):
        session = Session()
        c1 = session.query(schema.Category).filter_by(name='Televisions').first()
        session.close()
        r = requests.post('http://localhost:5000/category', json={'parent': 'cat.'+str(c1.id), 'name': 'api test 03'})
        self.assertEqual(r.status_code, 200)
        session = Session()
        c2 = session.query(schema.Category).filter_by(name='api test 03').first()
        session.close()
        self.assertEqual(c2.parent_id, c1.id)

    def test_04_create_category_error_1(self):
        r = requests.post('http://localhost:5000/category', json={'parent': 'itm.1', 'name': 'api test 04'})
        self.assertEqual(r.status_code, 400)

    def test_05_create_category_error_2(self):
        r = requests.post('http://localhost:5000/category', json={'parent': 'cat.1', 'text': 'api test 05'})
        self.assertEqual(r.status_code, 400)

    def test_06_create_item(self):
        session = Session()
        c1 = session.query(schema.Category).filter_by(name='api test 03').first()
        session.close()
        r = requests.post('http://localhost:5000/item', json={'parent': 'cat.'+str(c1.id), 'name': 'api test 06'})
        self.assertEqual(r.status_code, 200)
        session = Session()
        c2 = session.query(schema.Item).filter_by(label='api test 06').first()
        session.close()
        self.assertEqual(c2.category_id, c1.id)

    def test_07_create_item_error_1(self):
        r = requests.post('http://localhost:5000/item', json={'parent': 'itm.1', 'name': 'api test 07'})
        self.assertEqual(r.status_code, 400)

    def test_08_create_item_error_2(self):
        r = requests.post('http://localhost:5000/item', json={'parent': 'cat.1', 'text': 'api test 08'})
        self.assertEqual(r.status_code, 400)

    def test_09_update_category(self):
        session = Session()
        c1 = session.query(schema.Category).filter_by(name='Gaming consoles').first()
        c2 = session.query(schema.Category).filter_by(name='Electronics').first()
        session.close()
        parent_id = c2.id
        r = requests.put('http://localhost:5000/category', json={'parent': 'cat.'+str(parent_id), 'id': 'cat.'+str(c1.id)})
        self.assertEqual(r.status_code, 200)
        session = Session()
        c = session.query(schema.Category).filter_by(name='Gaming consoles').first()
        session.close()
        self.assertEqual(c.parent_id, parent_id)

    def test_10_update_category_error_1(self):
        r = requests.put('http://localhost:5000/category', json={'id': '2'})
        self.assertEqual(r.status_code, 400)

    def test_11_update_category_error_2(self):
        r = requests.put('http://localhost:5000/category', json={'parent': 'itm.1', 'id': '2'})
        self.assertEqual(r.status_code, 400)

    def test_12_update_item(self):
        session = Session()
        c1 = session.query(schema.Category).filter_by(name='Gaming consoles').first()
        c2 = session.query(schema.Category).filter_by(name='Televisions').first()
        i = session.query(schema.Item).filter_by(label='PS4 Pro').first()
        session.close()
        self.assertEqual(i.category_id, c1.id)
        parent_id = c2.id
        r = requests.put('http://localhost:5000/item', json={'parent': 'cat.'+str(parent_id), 'id': 'itm.'+str(i.id)})
        self.assertEqual(r.status_code, 200)
        session = Session()
        i = session.query(schema.Item).filter_by(label='PS4 Pro').first()
        session.close()
        self.assertEqual(i.category_id, parent_id)

    def test_13_update_item_error_1(self):
        r = requests.put('http://localhost:5000/item', json={'id': '2'})
        self.assertEqual(r.status_code, 400)

    def test_14_update_item_error_2(self):
        r = requests.put('http://localhost:5000/category', json={'parent': 'itm.1', 'id': '2'})
        self.assertEqual(r.status_code, 400)

if __name__ == '__main__':
    dbname = "dbtest"
    os.remove(dbname)
    schema.main(dbname)
    engine = create_engine("sqlite:///"+dbname, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        category1 = schema.Category(name='Electronics')
        session.add(category1)
        session.commit()
        category2 = schema.Category(name='Televisions', parent_id=category1.id)
        session.add(category2)
        session.commit()
        category3 = schema.Category(name='Gaming consoles')
        session.add(category3)
        session.commit()
        item1 = schema.Item(label='49-inch LCD', category_id=category2.id)
        session.add(item1)
        session.commit()
        item2 = schema.Item(label='40-inch plasma', category_id=category2.id)
        session.add(item2)
        session.commit()
        item3 = schema.Item(label='32-inch CRT', category_id=category2.id)
        session.add(item3)
        session.commit()
        item4 = schema.Item(label='PS4 Pro', category_id=category3.id)
        session.add(item4)
        session.commit()
        item5 = schema.Item(label='XBox One X', category_id=category3.id)
        session.add(item5)
        session.commit()
        item6 = schema.Item(label='Nintendo Switch', category_id=category3.id)
        session.add(item6)
        session.commit()
    except Exception as e:
        session.rollback()
        raise(e)
    unittest.main()
