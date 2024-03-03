from src.commands.authenticate import Authenticate
from src.session import Session, engine
from src.models.model import Base
from httmock import HTTMock
from src.errors.errors import ExternalError, Unauthorized
from uuid import uuid4
from tests.mocks import mock_failed_auth, mock_success_auth

class TestAuthenticate():
  def test_authenticate(self):
    with HTTMock(mock_success_auth):
      result = Authenticate(uuid4()).execute()
      assert 'id' in result

  def test_failed_authenticate(self):
    with HTTMock(mock_failed_auth):
      try:
        result = Authenticate('09322959-5bd7-4fdb-b262-ab46dab67c68').execute()
        assert False
      except Unauthorized:
        assert True
  