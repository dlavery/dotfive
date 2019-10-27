import os
import traceback
from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Category
from schema import Item
from functions import unpack_categories

if 'DB_NAME' in os.environ:
    DB_NAME = os.environ['DB_NAME']
else:
    raise Exception('DB name missing')

if 'API_HOST' in os.environ:
    API_HOST = os.environ['API_HOST']
else:
    API_HOST = os.environ['API_HOST']

app = Flask(__name__, static_url_path='')

engine = create_engine("sqlite:///"+DB_NAME, echo=False)
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    ''' Return static home page

        TODO: in a live environment there would be a separation between the
        UI application and the APIs
    '''
    return send_from_directory('', 'index.html')

@app.route('/categories', methods=['GET'])
def get_categories():
    ''' Eager load categories and items'''
    try:
        categories = []
        session = Session()
        data = []
        for c in session.query(Category).filter_by(parent_id=None).order_by(Category.name):
            data = unpack_categories(c, data)
        return jsonify(data)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'success': 'NOTOK'}), 500
    finally:
        session.close()

@app.route('/category', methods=['POST'])
def create_category():
    try:
        session = Session()
        if 'parent' not in request.json or 'name' not in request.json:
            return jsonify({'success': 'NOTOK'}), 400
        # Category at top level
        if len(request.json['parent']) < 5:
            category = Category(name=request.json['name'])
        else:
            # Category has a parent
            if (request.json['parent'][:3] != 'cat'):
                return jsonify({'success': 'NOTOK'}), 400
            parent_id = int(request.json['parent'][4:])
            category = Category(name=request.json['name'], parent_id=parent_id)
        session.add(category)
        session.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        session.rollback()
        print(traceback.format_exc())
        return jsonify({'success': 'NOTOK'}), 500
    finally:
        session.close()

@app.route('/category', methods=['PUT'])
def update_category():
    try:
        session = Session()
        if 'id' not in request.json or 'parent' not in request.json:
            return jsonify({'success': 'NOTOK'}), 400
        if (request.json['parent'][:3] != 'cat' or request.json['id'][:3] != 'cat'):
            return jsonify({'success': 'NOTOK'}), 400
        category_id = int(request.json['id'][4:])
        parent_id = int(request.json['parent'][4:])
        category = session.query(Category).filter_by(id=category_id).first()
        category.parent_id = parent_id
        session.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        session.rollback()
        print(traceback.format_exc())
        return jsonify({'success': 'NOTOK'}), 500
    finally:
        session.close()

@app.route('/item', methods=['POST'])
def create_item():
    try:
        session = Session()
        if 'parent' not in request.json \
        or 'name' not in request.json \
        or request.json['parent'][:3] != 'cat':
            return jsonify({'success': 'NOTOK'}), 400
        parent_id = int(request.json['parent'][4:])
        item = Item(label=request.json['name'], category_id=parent_id)
        session.add(item)
        session.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        session.rollback()
        print(traceback.format_exc())
        return jsonify({'success': 'NOTOK'}), 500
    finally:
        session.close()

@app.route('/item', methods=['PUT'])
def update_item():
    try:
        session = Session()
        if 'id' not in request.json or 'parent' not in request.json:
            return jsonify({'success': 'NOTOK'}), 400
        if (request.json['parent'][:3] != 'cat' or request.json['id'][:3] != 'itm'):
            return jsonify({'success': 'NOTOK'}), 400
        item_id = int(request.json['id'][4:])
        parent_id = int(request.json['parent'][4:])
        item = session.query(Item).filter_by(id=item_id).first()
        item.category_id = parent_id
        session.commit()
        return jsonify({'success': 'OK'})
    except Exception as e:
        session.rollback()
        print(traceback.format_exc())
        return jsonify({'success': 'NOTOK'}), 500
    finally:
        session.close()
