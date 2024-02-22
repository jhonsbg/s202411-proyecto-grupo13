import pytest
from score.src.commands.calcula import Create
from src.commands.autorizacion import Autorizacion
from src.errors.errors import AuthenticationException
import json
from flask import Response

class TestAutoriza():
    def test_autoriza(self):
        with pytest.raises(AuthenticationException) as exc_info:
            result_autoriza = Autorizacion(token='').execute()

        assert exc_info.type == AuthenticationException