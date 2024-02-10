from httmock import HTTMock, all_requests, response

@all_requests
def mock_success_auth(url, request):
  return response(200, { 'id': 1 }, {}, None, 5, request)

@all_requests
def mock_failed_auth(url, request):
  return { 'status_code': 401 }

@all_requests
def mock_success_auth_post(url, request):
  return response(201, { 'id': 1 }, {'Authorization': 'Bearer 12312312'}, None, 5, request)
