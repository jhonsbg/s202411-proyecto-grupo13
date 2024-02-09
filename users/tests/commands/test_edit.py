from src.commands.create import Create
from src.commands.edit import Edit
import json

class TestEdit():
  def test_edit(self):
    result = Create(
      json.loads(
        '{ "username": "vesta5", "password": "0tb3dpp8v69orsp", "email": "amalia5.crooks87@hotmail.com", "dni": "197", "fullName": "janie bayer", "phoneNumber": "9423002000" }'
        )).execute()
    
    result_edit = Edit(
      result["id"],
      json.loads(
        '{ "status": "POR_VERIFICAR", "dni": "199", "fullName": "marion welch", "phoneNumber": "5367864663" }'
        )).execute()
    
    assert result_edit == True