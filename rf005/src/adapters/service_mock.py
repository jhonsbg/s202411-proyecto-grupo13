from ..errors.errors import *

class ServiceMock():

    def resquest(self, method, path, headers, data):
        if 'users/me' in path:
            if headers["Authorization"] is None:
                raise AuthenticationException()
                
            if "fake" in headers["Authorization"]:
                raise BadRequestException()

            if headers["Authorization"] != "Bearer cd3d1303-2d62-4f60-8472-3349d34f690c":
                raise AuthenticationException()
            return MockResponse(200, self.getUserResponse)
        if '/posts/' in path:
            return MockResponse(200, self.getPostResponse)
        if '/routes/' in path:
            return MockResponse(200, self.getRouteResponse)
        if '/offers' in path:
            return MockResponse(200, self.getOfferResponse)
        if '/scores' in path:
            return MockResponse(200, self.getScoreResponse)
        else:
            return MockResponse(200, self.json)
    
    def json(self):
        return {
            "data": []
        }
    
    def getUserResponse(self):
        return {
            "id": "cd3d1303-2d62-4f60-8472-3349d34f690c"
        }
    
    def getPostResponse(self):
        return {'createdAt': '2024-03-01T22:26:13.632000', 'expireAt': '2024-03-08T22:26:13.608000', 'id': 'dbfac76e-30ed-4620-b97f-ebf9b0cd26a5', 'routeId': '15e854be-3101-4744-805c-257030be3a01', 'userId': 'cd3d1303-2d62-4f60-8472-3349d34f690c'}
    
    def getOfferResponse(self):
        return [{'createdAt': '2024-03-02T15:08:10.724235+00:00', 'description': 'dolores omnis inventore', 'fragile': False, 'id': '7319e258-c62f-42c7-a271-e3f4f95d1394', 'offer': 500, 'postId': 'dbfac76e-30ed-4620-b97f-ebf9b0cd26a5', 'size': 'Large', 'userId': 'dbe2025d-0f75-46ed-9a21-33496de983f3'}, {'createdAt': '2024-03-02T15:08:22.237463+00:00', 'description': 'distinctio occaecati quidem', 'fragile': True, 'id': 'c797421f-7930-4671-a3c3-8b1c602c9580', 'offer': 1000, 'postId': 'dbfac76e-30ed-4620-b97f-ebf9b0cd26a5', 'size': 'Large', 'userId': 'dbe2025d-0f75-46ed-9a21-33496de983f3'}]
    
    def getRouteResponse(self):
        return {'bagCost': 254, 'createdAt': '2024-03-01T22:26:12.576252+00:00', 'cupdateAt': '2024-03-01T22:26:12.576252+00:00', 'destinyAirportCode': 'LGW', 'destinyCountry': 'Inglaterra', 'flightId': '184', 'id': '15e854be-3101-4744-805c-257030be3a01', 'plannedEndDate': '2024-03-11T22:26:12.553000+00:00', 'plannedStartDate': '2024-03-03T22:26:12.553000+00:00', 'sourceAirportCode': 'BOG', 'sourceCountry': 'Colombia'}
    
    def getScoreResponse(self):
        return [{'id': '5f332274-f56c-418f-8fc3-897744bd15ce', 'offerid': 'c797421f-7930-4671-a3c3-8b1c602c9580', 'profit': 950, 'userid': 'e84ed78c-3837-4590-b88f-534dcbe39a63'}, {'id': 'f8972499-4bb0-42d1-b788-ea2ee1c173b8', 'offerid': '7319e258-c62f-42c7-a271-e3f4f95d1394', 'profit': 450, 'userid': 'e84ed78c-3837-4590-b88f-534dcbe39a63'}]
    
class MockResponse(): 
    def __init__(self, status_code, json_method):
        self.status_code = status_code
        self.json = json_method
