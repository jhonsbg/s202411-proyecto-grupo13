import pytest
from flask import Flask
from flask.testing import FlaskClient
from src.commands.create import Create

@pytest.fixture
def app():
    # Crea una aplicación Flask simple para usar en las pruebas
    return Flask(__name__)

@pytest.fixture
def client(app):
    # Crea un cliente de prueba para la aplicación Flask
    return app.test_client()

@pytest.fixture
def request_context(app):
    # Establece un contexto de solicitud para las pruebas
    with app.test_request_context():
        yield

class TestCreate():

    def test_is_valid_token(self):
        create = Create({})
        assert create.is_valid_token("Bearer cd3d1303-2d62-4f60-8472-3349d34f690c") == True


    
