from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.models.post import Post
from src.errors.errors import IncompleteParams, InvalidDates
from datetime import datetime, timedelta

class TestCreatePost():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  # def test_create_post(self):
  #   data = {
  #     'routeId': '1',
  #     'expireAt': "2024-02-17T02:21:49.025Z"
  #   }
  #   userId = '09322959-5bd7-4fdb-b262-ab46dab67c68'
  #   post = CreatePost(data, userId).execute()

  #   assert str(post['routeId']) == data['routeId']
  #   assert post['userId'] == userId
  #   assert 'createdAt' in post

  def test_create_post_missing_fields(self):
    try:
      CreatePost({}).execute()
      assert False
    except IncompleteParams:
      assert True

  def test_create_post_invalid_dates(self):
    try:
      data = {
        'routeId': '1',
        'expireAt': "2024-02-08T02:21:49.025Z"
      }
      userId = '09322959-5bd7-4fdb-b262-ab46dab67c68'
      CreatePost(data, userId).execute()
      assert False
    except InvalidDates:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)