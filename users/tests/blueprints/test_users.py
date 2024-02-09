from src.main import app
import json
import os

class TestUsers():

  def test_reset(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/users/reset', json={}
      )

      assert response.status_code == 200


  def test_create_user(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/users', json={
            'username': 'vesta',
            'password': '0tb3dpp8v69orsp',
            'email': 'amalia.crooks87@hotmail.com',
            'dni': '197',
            'fullName': 'janie bayer',
            'phoneNumber': '9423002000'
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 201
      assert 'id' in response_json
      self.id = response_json['id']
      assert 'createdAt' in response_json

      # test_create_existing_user
      response = test_client.post(
        '/users', json={
            'username': 'vesta',
            'password': '0tb3dpp8v69orsp',
            'email': 'amalia.crooks87@hotmail.com',
            'dni': '197',
            'fullName': 'janie bayer',
            'phoneNumber': '9423002000'
        }
      )

      assert response.status_code == 412

      #test_create_user_missing_fields
      response = test_client.post(
        '/users', json={
            'fullName': 'janie bayer',
        }
      )

      assert response.status_code == 400

  def test_edit_user(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/users', json={
            'username': 'vesta2',
            'password': '0tb3dpp8v69orsp2',
            'email': 'amalia2.crooks87@hotmail.com',
            'dni': '1972',
            'fullName': 'janie bayer 2',
            'phoneNumber': '9423002002'
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 201
      assert 'id' in response_json
      id = response_json['id']

      response = test_client.patch(
        '/users/{}'.format(id) , json={
            'status': 'POR_VERIFICAR',
            'dni': '199',
            'fullName': 'marion welch',
            'phoneNumber': '5367864663'
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 200
      assert 'msg' in response_json
      assert response_json['msg'] == 'el usuario ha sido actualizado'

      # test_edit_missing_fields
      response = test_client.patch(
        '/users/{}'.format(id) , json={}
      )

      assert response.status_code == 400

      # test_edit_invalid_fields
      response = test_client.patch(
        '/users/{}'.format(id) , json={'email': 'amalia2.crooks87@hotmail.com'}
      )

      assert response.status_code == 400

      # test_edit_invalid_user
      response = test_client.patch(
        '/users/{}'.format('bf8792d2-3097-11ee-be56-0242ac120003') , json={
            'status': 'POR_VERIFICAR',
            'dni': '199',
            'fullName': 'marion welch',
            'phoneNumber': '5367864663'
        }
      )

      assert response.status_code == 404

  def test_generate_token(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/users/auth', json={
            'username': 'vesta',
            'password': '0tb3dpp8v69orsp'
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 200
      assert 'id' in response_json
      assert 'token' in response_json
      assert 'expireAt' in response_json

      # test_wrong_password
      response = test_client.post(
        '/users/auth', json={
            'username': 'vesta',
            'password': 'wrong'
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 404

      # test_invalid_user
      response = test_client.post(
        '/users/auth', json={
            'username': 'fake',
            'password': 'fake'
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 404

      # test_missing_fields
      response = test_client.post(
        '/users/auth', json={
            'username': 'vesta',
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 400

  def test_me(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/users', json={
            'username': 'vesta3',
            'password': '0tb3dpp8v69orsp3',
            'email': 'amalia3.crooks87@hotmail.com',
            'dni': '1973',
            'fullName': 'janie bayer 3',
            'phoneNumber': '9423002003'
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 201
      assert 'id' in response_json
      id = response_json['id']

      response = test_client.get(
        '/users/me', headers={"Authorization": "Bearer {}".format(id)}
      )
      response_json = json.loads(response.data)

      assert response.status_code == 200
      assert 'username' in response_json
      assert 'password' in response_json
      assert 'email' in response_json
      assert 'dni' in response_json
      assert 'fullName' in response_json
      assert 'phoneNumber' in response_json

      # test_invalid_token
      response = test_client.get(
        '/users/me', headers={"Authorization": "Bearer {}fake".format(id)}
      )

      assert response.status_code == 401

  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get('/users/ping')

      assert response.status_code == 200