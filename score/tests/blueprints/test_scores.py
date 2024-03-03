from src.main import app
import json

class TestScores():

    def test_reset(self):
        with app.test_client() as test_client:
            response = test_client.post(
                '/scores/reset', json={}
            )

        assert response.status_code == 200
    
    def test_ping(self):
        with app.test_client() as test_client:
            response = test_client.get('/scores/ping')

        assert response.status_code == 200

    def test_calculate(self):
        token = "Bearer cd3d1303-2d62-4f60-8472-3349d34f690c"
        with app.test_client() as test_client:
            response = test_client.post(
                '/scores', json={
                'userid': 'd3d1303-2d62-4f60-8472-3349d34f690c',
                'offerid': 'fake_offer',
                'offer': 100,
                'size': 'LARGE',
                'bagCost': 50,
                },
                headers={'Authorization': token}
            )
        response_json = json.loads(response.data)

        assert response.status_code == 201
        assert response_json['profit'] == 50

        with app.test_client() as test_client:
            response = test_client.post(
                '/scores', json={
                'userid': 'd3d1303-2d62-4f60-8472-3349d34f690c',
                'offerid': 'fake_offer',
                'offer': 150,
                'size': 'MEDIUM',
                'bagCost': 50,
                },
                headers={'Authorization': token}
            )
        response_json = json.loads(response.data)

        assert response.status_code == 201
        assert response_json['profit'] == 125

        with app.test_client() as test_client:
            response = test_client.post(
                '/scores', json={
                'userid': 'd3d1303-2d62-4f60-8472-3349d34f690c',
                'offerid': 'fake_offer',
                'offer': 20,
                'size': 'SMALL',
                'bagCost': 7,
                },
                headers={'Authorization': token}
            )
        response_json = json.loads(response.data)

        assert response.status_code == 201
        assert response_json['profit'] == 18.25

        with app.test_client() as test_client:
            response = test_client.get('/scores', headers={'Authorization': token})
        
        response_json = json.loads(response.data)


        assert response.status_code == 200
        assert len(response_json) == 3
    