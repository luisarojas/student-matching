# graph_server/__init__.py

from flask import Flask
from flask_restful import Api
from py2neo import Graph

import os

app = Flask(__name__)
api = Api(app)

# Configure the app settings
app_settings = os.getenv(
        'APP_SETTINGS',
        'graph_server.config.TestConfig'
)
app.config.from_object(app_settings)

# Create graph connection
graph = Graph(**app.config.get('GRAPH_DATABASE_URI'))

from graph_server import views
