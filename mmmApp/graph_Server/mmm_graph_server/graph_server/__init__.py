# graph_server/__init__.py

from flask import Flask
from flask_restful import Resource, Api
from py2neo import Graph

import os

app = Flask(__name__)
api = Api(app)

app_settings = os.getenv(
        'APP_SETTINGS',
        'graph_server.config.BaseConfig'
)
app.config.from_object(app_settings)

graph = Graph(**app.config.get('GRAPH_DATABASE_URI'))

from graph_server import view
