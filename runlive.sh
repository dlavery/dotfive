#!/bin/sh
export FLASK_APP=app.py
export DB_NAME=dblive
export API_HOST=localhost
flask run
