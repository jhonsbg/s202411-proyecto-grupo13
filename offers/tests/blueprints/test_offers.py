from src.main import app
import json

class TestOffers():

    def test_reset(self):
        with app.test_client() as test_client:
            response = test_client.post(
                '/offers/reset', json={}
            )

        assert response.status_code == 200
    
    def test_create_offer(self):
        with app.test_client() as test_client:
            headers = {'Authorization': 'Bearer cd3d1303-2d62-4f60-8472-3349d34f690c'}
            response = test_client.post(
                '/offers', json={
                    "postId": "57b545b2-0c22-4415-b58c-69c521433484",
                    "description": "mi primera oferta",
                    "size": "LARGE",
                    "fragile": True,
                    "offer": 303
                },
                headers=headers
            )
        response_json = json.loads(response.data)

        assert response.status_code == 201
        assert 'id' in response_json
        self.id = response_json['id']
        assert 'createdAt' in response_json

        #Test tamaño del paquete no valida oferta negativa
        response = test_client.post(
            '/offers', json={
                    "postId": "57b545b2-0c22-4415-b58c-69c521433484",
                    "description": "mi primera oferta",
                    "size": "Wide",
                    "fragile": True,
                    "offer": -303
                },
                headers=headers
        )

        assert response.status_code == 412

    #Test obtener listado de ofertas
    def test_get_offers(self):
        with app.test_client() as test_client:
            headers = {'Authorization': 'Bearer cd3d1303-2d62-4f60-8472-3349d34f690c'}
            response = test_client.get(
                '/offers', headers=headers
            ),
        response_json = json.loads(response[0].data)

        assert response[0].status_code == 200
        assert any('description' in offer for offer in response_json)
        assert isinstance(response_json, list)
        assert len(response_json) > 0
    
    def test_ping(self):
        with app.test_client() as test_client:
            response = test_client.get('/offers/ping')

            assert response.status_code == 200
    
