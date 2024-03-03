from ..errors.errors import *

class ServiceMock():

    def resquest(self, method, path, headers, data):
        
        if 'users/me' in path:
            if headers["Authorization"] is None:
                raise NoTokenRequest()
                
            if "fake" in headers["Authorization"]:
                raise Unauthorized()

            
            print(headers["Authorization"])

            if headers["Authorization"] != "Bearer cd3d1303-2d62-4f60-8472-3349d34f690c":
                raise Unauthorized()
            return MockResponse(200, self.getUserResponse)
        if '/posts' in path and method == 'get':
            return MockResponse(201, self.getPostResponse)
        if '/posts' in path and method == 'post':
            return MockResponse(201, self.postPostResponse)
        if '/routes' in path:
            return MockResponse(200, self.getRouteResponse)
       
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
        return [{'createdAt': '2024-03-03T17:39:52.808000', 'expireAt': '2024-03-04T17:39:52.637000', 'id': 'eb76195f-74f5-4f49-8060-7bcc61e0ec09', 'routeId': 'ba538afd-c070-42d3-946f-04f2d2cb9876', 'userId': '826b074f-ea2b-499e-aadb-d9ea1420e3cc'}, {'createdAt': '2024-03-03T17:39:53.747000', 'expireAt': '2024-03-04T17:39:53.601000', 'id': 'e8d006c6-fb68-495a-80f1-75c2c80c6dff', 'routeId': '700c0623-fae4-49ad-9c95-3bba30995f75', 'userId': '826b074f-ea2b-499e-aadb-d9ea1420e3cc'}, {'createdAt': '2024-03-03T19:24:21.603000', 'expireAt': '2024-03-04T19:24:21.319000', 'id': '92f4a05e-d543-4ae9-9753-5e95e41fa3ed', 'routeId': '37defc63-f738-40ec-8471-0f71b9b4da25', 'userId': '826b074f-ea2b-499e-aadb-d9ea1420e3cc'}]
     
    def getRouteResponse(self):
        return [{'bagCost': 390, 'createdAt': '2024-03-03T17:39:52.476139+00:00', 'cupdateAt': '2024-03-03T17:39:52.476139+00:00', 'destinyAirportCode': 'LGW', 'destinyCountry': 'Inglaterra', 'flightId': '658', 'id': 'ba538afd-c070-42d3-946f-04f2d2cb9876', 'plannedEndDate': '2024-03-13T17:39:52.445000+00:00', 'plannedStartDate': '2024-03-05T17:39:52.445000+00:00', 'sourceAirportCode': 'BOG', 'sourceCountry': 'Colombia'}, {'bagCost': 176, 'createdAt': '2024-03-03T17:39:53.712852+00:00', 'cupdateAt': '2024-03-03T17:39:53.712852+00:00', 'destinyAirportCode': 'LGW', 'destinyCountry': 'Inglaterra', 'flightId': '463', 'id': '414c7de2-9682-47f7-98e3-beea9d633f3a', 'plannedEndDate': '2024-03-13T17:39:53.600000+00:00', 'plannedStartDate': '2024-03-05T17:39:53.600000+00:00', 'sourceAirportCode': 'BOG', 'sourceCountry': 'Colombia'}, {'bagCost': 245, 'createdAt': '2024-03-03T19:24:21.570738+00:00', 'cupdateAt': '2024-03-03T19:24:21.570738+00:00', 'destinyAirportCode': 'LGW', 'destinyCountry': 'Inglaterra', 'flightId': '510X', 'id': 'd6c48381-0166-47de-8276-ebd70f388dd5', 'plannedEndDate': '2024-03-13T19:24:21.317000+00:00', 'plannedStartDate': '2024-03-05T19:24:21.317000+00:00', 'sourceAirportCode': 'BOG', 'sourceCountry': 'Colombia'}]
    
    def postPostResponse(self):
        return {'createdAt': '2024-03-03T19:27:25.987000', 'expireAt': '2024-03-04T19:27:25.881000', 'id': 'ddeb3f35-c430-4b6e-9035-e182d793de5c', 'routeId': '1736ef40-d3bd-4086-bf5f-6eef6bcb6ca1', 'userId': '826b074f-ea2b-499e-aadb-d9ea1420e3cc'}
     
    def postRouteResponse(self):
        return [{'bagCost': 390, 'createdAt': '2024-03-03T17:39:52.476139+00:00', 'cupdateAt': '2024-03-03T17:39:52.476139+00:00', 'destinyAirportCode': 'LGW', 'destinyCountry': 'Inglaterra', 'flightId': '658', 'id': 'ba538afd-c070-42d3-946f-04f2d2cb9876', 'plannedEndDate': '2024-03-13T17:39:52.445000+00:00', 'plannedStartDate': '2024-03-05T17:39:52.445000+00:00', 'sourceAirportCode': 'BOG', 'sourceCountry': 'Colombia'}, {'bagCost': 176, 'createdAt': '2024-03-03T17:39:53.712852+00:00', 'cupdateAt': '2024-03-03T17:39:53.712852+00:00', 'destinyAirportCode': 'LGW', 'destinyCountry': 'Inglaterra', 'flightId': '463', 'id': '414c7de2-9682-47f7-98e3-beea9d633f3a', 'plannedEndDate': '2024-03-13T17:39:53.600000+00:00', 'plannedStartDate': '2024-03-05T17:39:53.600000+00:00', 'sourceAirportCode': 'BOG', 'sourceCountry': 'Colombia'}, {'bagCost': 245, 'createdAt': '2024-03-03T19:24:21.570738+00:00', 'cupdateAt': '2024-03-03T19:24:21.570738+00:00', 'destinyAirportCode': 'LGW', 'destinyCountry': 'Inglaterra', 'flightId': '510X', 'id': 'd6c48381-0166-47de-8276-ebd70f388dd5', 'plannedEndDate': '2024-03-13T19:24:21.317000+00:00', 'plannedStartDate': '2024-03-05T19:24:21.317000+00:00', 'sourceAirportCode': 'BOG', 'sourceCountry': 'Colombia'}]
    
class MockResponse(): 
    def __init__(self, status_code, json_method):
        self.status_code = status_code
        self.json = json_method
