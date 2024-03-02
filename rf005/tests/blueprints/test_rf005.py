from src.main import app
import json

class TestRF005():

  def test_get_post(self):
    with app.test_client() as test_client:
      response = test_client.get(
        '/rf005/posts/test_id',
        headers={
          'Authorization': 'Bearer cd3d1303-2d62-4f60-8472-3349d34f690c'
        },
      )

      assert response.status_code == 200

      response_json = json.loads(response.data)

      assert 'data' in response_json
      assert 'offers' in response_json['data']
      assert 'route' in response_json['data']
      assert 'createdAt' in response_json['data']
      assert 'expireAt' in response_json['data']
      assert 'id' in response_json['data']
      assert 'plannedEndDate' in response_json['data']
      assert 'plannedStartDate' in response_json['data']

      assert len(response_json['data']["offers"]) == 2
      assert response_json['data']["offers"][0]["score"] > response_json['data']["offers"][1]["score"]



  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get('/rf005/ping')

      assert response.status_code == 200