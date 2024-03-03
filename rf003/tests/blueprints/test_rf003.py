from src.main import app
import json

class TestRF003():

  def test_create_post(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/rf003/posts',
        headers={
          'Authorization': 'Bearer cd3d1303-2d62-4f60-8472-3349d34f690c'
        },
        json={
            "flightId": "658",
            "expireAt": "2025-02-04T19:27:25.000Z",
            "plannedStartDate": "2025-03-05T19:27:25.000Z",
            "plannedEndDate": "2025-03-13T19:27:25.000Z",
            "origin": {
              "airportCode": "BOG",
              "country": "Colombia"
            },
            "destiny": {
              "airportCode": "LGW",
              "country": "Inglaterra"
            },
            "bagCost": 944
        }
      )

      assert response.status_code == 201

      response_json = json.loads(response.data)

      assert 'data' in response_json
      assert 'route' in response_json['data']
      assert 'createdAt' in response_json['data']
      assert 'expireAt' in response_json['data']
      assert 'id' in response_json['data']
      assert 'userId' in response_json['data']
      assert 'id' in response_json['data']['route']

  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get('/rf003/ping')

      assert response.status_code == 200