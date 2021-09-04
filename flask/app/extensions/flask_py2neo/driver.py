from __future__ import absolute_import
from logging import exception
from flask import current_app, _app_ctx_stack
from py2neo import Graph
from py2neo.ogm import Repository
import neo4j

__version__ = "0.2.0"


class Flask_Py2Neo(object):
    current_app = None
    transaction = None

    def __init__(self, app=None):
        self.current_app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.current_app = app
        """This callback can be used to initialize an application for the
        use with this database setup.
        """
        app.config.setdefault("NEO4J_BOLT", False)
        app.config.setdefault("NEO4J_SECURE", False)
        app.config.setdefault("NEO4J_CERT_CHECK", False)
        app.config.setdefault('NEO4J_ROUTING', False)
        app.config.setdefault("NEO4J_HTTP_PORT", 7474)
        app.config.setdefault("NEO4J_HTTPS_PORT", 7473)
        app.config.setdefault("NEO4J_BOLT_PORT", 7687)
        app.config.setdefault("NEO4J_HOST", 'localhost')
        app.config.setdefault("NEO4J_USER", "neo4j")
        app.config.setdefault("NEO4J_PASSWORD", "neo4j")
        
        _neo4j_scheme_selection = self.get_neo4j_uri_scheme(app)
        _py2neo_scheme = _neo4j_scheme_selection["PY2NEO_URI"]
        _neo4j_scheme = _neo4j_scheme_selection["NEO4J_URI"]
        _host = app.config["NEO4J_HOST"]
        _port = _neo4j_scheme_selection["PORT"]
        _py2neo_uri = f'{_py2neo_scheme}://{_host}:{_port}'
        _neo4j_uri = f'{_neo4j_scheme}://{_host}:{_port}'

        app.config.setdefault("PY2NEO_URI", _py2neo_uri)
        app.config.setdefault("NEO4J_URI", _neo4j_uri)
        app.extensions["py2neo_graph", 'py2neo_repo', 'neo4j'] = self
        self._begin()

    def get_neo4j_uri_scheme(self, app):
        if app.config["NEO4J_BOLT"] is True and app.config["NEO4J_ROUTING"] is False:
            if app.config["NEO4J_SECURE"] is False:
                return {'NEO4J_URI':'bolt','PY2NEO_URI': 'bolt', 'PORT': app.config["NEO4J_BOLT_PORT"]}
            if app.config["NEO4J_SECURE"] is True and app.config["NEO4J_CERT_CHECK"] is True:
                return {'PY2NEO_URI': 'bolt+s', 'PORT': app.config["NEO4J_BOLT_PORT"]}
            if app.config["NEO4J_SECURE"] is True and app.config["NEO4J_CERT_CHECK"] is False:
                return {'PY2NEO_URI': 'bolt+ssc', 'PORT': app.config["NEO4J_BOLT_PORT"]}
        if app.config["NEO4J_BOLT"] is False:
            if app.config["NEO4J_SECURE"] is False and app.config["NEO4J_ROUTING"] is False:
                return {'NEO4J_URI':'neo4j','PY2NEO_URI': 'http', 'PORT': app.config["NEO4J_HTTP_PORT"]}
            if app.config["NEO4J_SECURE"] is True and app.config["NEO4J_CERT_CHECK"] is True:
                return {'NEO4J_URI':'neo4j+s','PY2NEO_URI': 'https', 'PORT': app.config["NEO4J_HTTPS_PORT"]}
            if app.config["NEO4J_SECURE"] is True and app.config["NEO4J_CERT_CHECK"] is False:
                return {'NEO4J_URI':'neo4j+ssc','PY2NEO_URI': 'http+ssc', 'PORT': app.config["NEO4J_HTTPS_PORT"]}
        
        ###Write exception
        # if app.config["NEO4J_BOLT"] is True and app.config["NEO4J_ROUTING"] is True:
            
        #     pass


    @property
    def graph(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'py2neo_graph'):
                ctx.py2neo_graph = self._graph_connect
            return ctx.py2neo_graph

    @property
    def _graph_connect(self):
        return Graph(
            self.current_app.config["PY2NEO_URI"],
            auth=(self.current_app.config["NEO4J_USER"],
            self.current_app.config["NEO4J_PASSWORD"]))
    
    def _begin(self):
        self._graph_connect.begin

    @property
    def repo(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'py2neo_repo'):
                ctx.py2neo_repo = self._repo_connect
            return ctx.py2neo_repo

    @property
    def _repo_connect(self):
        return Repository(
            self.current_app.config["PY2NEO_URI"],
            auth=(self.current_app.config["NEO4J_USER"],
            self.current_app.config["NEO4J_PASSWORD"]))

    @property
    def neo4j_driver(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'neo4j'):
                ctx.neo4j = self._neo4j_connect
            return ctx.neo4j

    @property
    def _neo4j_connect(self):
        return neo4j.GraphDatabase.driver(
            self.current_app.config["NEO4J_URI"],
            auth=(self.current_app.config["NEO4J_USER"],
            self.current_app.config["NEO4J_PASSWORD"]))