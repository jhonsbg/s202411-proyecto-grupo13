from src.commands.create_post_public import CreatePostPublic
from src.session import Session, engine
from src.models.model import Base
from src.main import app
from src.models.post import Post
import json
from src.errors.errors import IncompleteParams, InvalidDates, PostCreateError
from datetime import datetime, timedelta
from uuid import uuid4
from httmock import HTTMock
from tests.mocks import mock_failed_auth, mock_success_auth, mock_success_auth_post


class TestCreatePostPublic():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_post_invalid_dates(self):
    try:
      data = {
        'origin': "BOG",
        'destiny': "MAD",
        'bagCost': 25,
        'plannedStartDate': datetime.now().date().isoformat(),
        'plannedEndDate': (datetime.now() + timedelta(days=1)).date().isoformat()
      }
      userId = 1
      token ="string"
      post = CreatePostPublic(data, userId, token).execute()
      assert False
    except InvalidDates:
      assert True

  def test_create_post_missing_fields(self):
    try:
      CreatePostPublic({}).execute()
      assert False
    except IncompleteParams:
      assert True

  def test_create_post_badrequest(self):
    try: 
      data = {
        'origin': "BOG",
        'bagCost': 25,
        'destiny': "MAD",   
        'plannedStartDate': (datetime.now() + timedelta(days=1)).date().isoformat(),
        'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
      }
      userId = 1
      token ="string"
      post = CreatePostPublic(data, userId, token).execute()

      assert False
    except IncompleteParams:
      assert True

  def test_missing_field2(self):
    try:
      with app.test_client() as test_client: 
        with HTTMock(mock_success_auth_post):
          data = {
            'origin': {'airportCode': 'LAX', 'country': 'USA'},
            'destiny': {'airportCode': 'BOG', 'country': 'CO'},
            'plannedStartDate': (datetime.now() + timedelta(days=1)).date().isoformat(),
            'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
          }
          userId = 1
          token ="string"
          post = CreatePostPublic(data=data, userId=userId, token= token).execute()
    except IncompleteParams:
      assert True

  def test_create_post(self):
    with app.test_client() as test_client: 
      with HTTMock(mock_success_auth_post):
        data = {
          'origin': {'airportCode': 'LAX', 'country': 'USA'},
          'destiny': {'airportCode': 'BOG', 'country': 'CO'},
          'bagCost': 25,
          'plannedStartDate': (datetime.now() + timedelta(days=1)).date().isoformat(),
          'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
        }
        userId = 1
        token ="string"
        post = CreatePostPublic(data=data, userId=userId, token= token).execute()

        assert post['routeId'] is not None
        assert post['userId'] == userId
        assert 'plannedStartDate' in post
        assert 'plannedEndDate' in post
  def test_create_post2(self):
    with app.test_client() as test_client: 
      with HTTMock(mock_success_auth_post):
        data = {
          'origin': {'airportCode': 'LAX', 'country': 'USA'},
          'destiny': {'airportCode': 'BOG', 'country': 'CO'},
          'bagCost': 25,
          'plannedStartDate': (datetime.now() + timedelta(days=1)).date().isoformat(),
          'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
        }
        userId = 1
        token ="string"
        post = CreatePostPublic(data=data, userId=userId, token= token).execute()
        try:
          with app.test_client() as test_client: 
            with HTTMock(mock_success_auth_post):
              data2 = {
                'origin': {'airportCode': 'LAX', 'country': 'USA'},
                'destiny': {'airportCode': 'BOG', 'country': 'CO'},
                'bagCost': 25,
                'plannedStartDate': (datetime.now() + timedelta(days=1)).date().isoformat(),
                'plannedEndDate': (datetime.now() + timedelta(days=2)).date().isoformat()
              }
              userId2 = 1
              token2 ="string"
              post2 = CreatePostPublic(data=data2, userId=userId2, token= token2).execute()
        except PostCreateError:
            assert True


  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)