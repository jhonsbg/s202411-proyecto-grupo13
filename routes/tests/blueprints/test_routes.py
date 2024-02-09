from src.main import app
import json
import os
from datetime import datetime, timezone, timedelta

class TestRoutes():

    def test_reset(self):
        with app.test_client() as test_client:
            response = test_client.post(
                '/routes/reset', json={}
            )

        assert response.status_code == 200
    
    def test_ping(self):
        with app.test_client() as test_client:
            response = test_client.get('/routes/ping')

        assert response.status_code == 200

    def test_crea_route(self):
        current_utc_time = datetime.now(timezone.utc)
        dateStart = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        current_utc_time = datetime.now(timezone.utc) + timedelta(days=5)
        dateEnd = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        with app.test_client() as test_client:
            response = test_client.post(
                '/routes', json={
                'flightId': '194',
                'sourceAirportCode': 'BOG',
                'sourceCountry': 'Colombia',
                'destinyAirportCode': 'LOW',
                'destinyCountry': 'Inglaterra',
                'bagCost': 386,
                'plannedStartDate': f'{dateStart}',
                'plannedEndDate': f'{dateEnd}'
                }
            )
        response_json = json.loads(response.data)

        assert response.status_code == 403

        token = "Bearer 39fb8604-7a9f-44b5-88d2-4be1ec9efba2"
        
        with app.test_client() as test_client:
            response = test_client.post(
                '/routes', json={
                'flightId': '194',
                'sourceAirportCode': 'BOG',
                'sourceCountry': 'Colombia',
                'destinyAirportCode': 'LOW',
                'destinyCountry': 'Inglaterra',
                'bagCost': 386,
                'plannedStartDate': f'{dateStart}',
                'plannedEndDate': f'{dateEnd}'
                },
                headers={'Authorization': token}
            )
        response_json = json.loads(response.data)

        assert response.status_code == 401

        token = "Bearer 39fb8604-7a9f-44b5-88d2-4be1ec9efba2"
        
        with app.test_client() as test_client:
            response = test_client.post(
                '/routes', json={
                'sourceAirportCode': 'BOG',
                'sourceCountry': 'Colombia',
                'destinyAirportCode': 'LOW',
                'destinyCountry': 'Inglaterra',
                'bagCost': 386,
                'plannedStartDate': f'{dateStart}',
                'plannedEndDate': f'{dateEnd}'
                },
                headers={'Authorization': token}
            )
        response_json = json.loads(response.data)

        assert response.status_code == 401

    def test_elimina_route(self):        
        with app.test_client() as test_client:
            response = test_client.delete('/routes/194')
        response_json = json.loads(response.data)

        assert response.status_code == 403

        token = "Bearer 39fb8604-7a9f-44b5-88d2-4be1ec9efba2"
        
        with app.test_client() as test_client:
            response = test_client.delete('/routes/194',
                headers={'Authorization': token}
            )
        response_json = json.loads(response.data)

        assert response.status_code == 401

    def test_consulta_route(self):        
        with app.test_client() as test_client:
            response = test_client.get('/routes/194')
        response_json = json.loads(response.data)

        assert response.status_code == 403

        token = "Bearer 39fb8604-7a9f-44b5-88d2-4be1ec9efba2"
        
        with app.test_client() as test_client:
            response = test_client.get('/routes/194',
                headers={'Authorization': token}
            )
        response_json = json.loads(response.data)

        assert response.status_code == 401

    def test_filtra_route(self):        
        with app.test_client() as test_client:
            response = test_client.get('/routes?flight=194')
        response_json = json.loads(response.data)

        assert response.status_code == 403

        token = "Bearer 39fb8604-7a9f-44b5-88d2-4be1ec9efba2"
        
        with app.test_client() as test_client:
            response = test_client.get('/routes?flight=194',
                headers={'Authorization': token}
            )
        response_json = json.loads(response.data)

        assert response.status_code == 401