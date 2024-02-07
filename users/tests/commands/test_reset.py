from src.commands.reset import Reset

class TestReset():
  def test_reset(self):
    result = Reset().execute()
    assert result == True

  