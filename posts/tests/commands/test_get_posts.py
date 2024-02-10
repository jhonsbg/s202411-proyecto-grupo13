import pytz
from src.commands.get_posts import GetPosts
from src.commands.create_post import CreatePost
from src.session import Session, engine
from src.models.model import Base
from src.models.post import Post
from src.errors.errors import InvalidParams
from datetime import datetime, timedelta

class TestGetPosts():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    self.post_data = {
      'routeId': '1',
      'expireAt': "2024-02-17T02:21:49.025Z"
    }
    self.userId = '09322959-5bd7-4fdb-b262-ab46dab67c68'
    self.post = CreatePost(self.post_data, self.userId).execute()

  # def test_get_posts(self):
  #   data = {
  #     'expire': 'false',
  #     'routeId': 1,
  #     'owner': 'me'
  #   }
  #   posts = GetPosts(data, self.userId).execute()
  #   assert len(posts) == 1

  #   posts = GetPosts(data, self.userId).execute()
  #   assert len(posts) > 0

  def test_get_posts_invalid_dates(self):
    try:
      data = {
        'expire': 'invalid',
        'routeId': '1',
        'owner': 'me'
      }
      GetPosts(data, self.userId).execute()
      assert False
    except InvalidParams:
      assert True

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)
