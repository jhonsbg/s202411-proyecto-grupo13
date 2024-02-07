from src.commands.create import Create
import json

class TestCreate():
  def test_create(self):
    result = Create(
      json.loads(
        '{ "username": "vesta4", "password": "0tb3dpp8v69orsp", "email": "amalia4.crooks87@hotmail.com", "dni": "197", "fullName": "janie bayer", "phoneNumber": "9423002000" }'
        )).execute()
    
    assert 'id' in result
    assert 'createdAt' in result

  