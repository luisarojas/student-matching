# mmm_graph_server/config.py

import os

# Create auth endpoint
authorization_endpoint = ('http://' +
                          str(os.getenv('AUTH_SERVER_HOST')) +
                          ':' +
                          str(os.getenv('AUTH_SERVER_PORT')) +
                          '/auth/status')

# Connect to the graph
graph_endpoint = {'bolt': True,
                  'host': os.getenv('DB_HOST', 'localhost'),
                  'user': os.getenv('DB_USER', 'neo4j'),
                  'password': os.getenv('DB_PSWD')}


class BaseConfig:
    """Base configuration"""
    AUTH_DATABASE_URI = authorization_endpoint
    PORT = os.getenv('SERVER_PORT', 5002)
    GRAPH_DATABASE_URI = graph_endpoint

class TestConfig(BaseConfig):
    GRAPH_DATABASE_URI = {'bolt': True,
                          'host': os.getenv('DB_HOST', 'localhost'),
                          'user': os.getenv('DB_USER', 'neo4j')}
# class DevelopmentConfig(BaseConfig):
