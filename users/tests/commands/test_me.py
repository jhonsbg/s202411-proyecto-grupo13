from src.commands.create import Create
from src.commands.me import Me
import json

class TestMe():
  def test_me(self):
    result = Create(
      json.loads(
        '{ "username": "vesta6", "password": "0tb3dpp8v69orsp", "email": "amalia6.crooks87@hotmail.com", "dni": "197", "fullName": "janie bayer", "phoneNumber": "9423002000" }'
        )).execute()
    
    result_me = Me("Bearer {}".format(result["id"])).execute()
    
    assert result_me.id is not None