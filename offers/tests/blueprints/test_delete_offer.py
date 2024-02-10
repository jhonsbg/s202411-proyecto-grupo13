from src.main import app
import json

class TestOffers():

#Test eliminar oferta con id invalido
    def test_delete_offers(self):
        offer_id = '57b545b2-0c22-4415-b58c-69c888888888'
        with app.test_client() as test_client:
            headers = {'Authorization': 'Bearer cd3d1303-2d62-4f60-8472-3349d34f690c'}
            response = test_client.delete(
                f'/offers/{offer_id}', headers=headers
            )

            assert response.status_code == 404
            assert 'mssg' in response.get_json()
            assert 'Data not found' in response.get_json().get('mssg', '')