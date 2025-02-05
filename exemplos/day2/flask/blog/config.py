import os
from dynaconf import FlaskDynaconf

HERE = os.path.dirname(os.path.abspath(__file__))

def configure(app):
    FlaskDynaconf(app, extensions_list="EXTENSION", root_path=HERE)
