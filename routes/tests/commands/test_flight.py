# import pytest
# from src.commands.crea import Create
# from src.commands.flight import VerFligth
# from src.errors.errors import SolicitudException
# import json
# from datetime import datetime, timezone, timedelta
# from flask import Response

# class TestConsulta():
#   def test_consulta(self):
#     current_utc_time = datetime.now(timezone.utc)
#     dateStart = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
#     current_utc_time = datetime.now(timezone.utc) + timedelta(days=5)
#     dateEnd = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
#     result = Create(
#     json.loads('''
#         {
#             "flightId": "10",
#             "sourceAirportCode": "BOG",
#             "sourceCountry": "Colombia",
#             "destinyAirportCode": "LOW",
#             "destinyCountry": "Inglaterra",
#             "bagCost": 386,
#             "plannedStartDate": "''' + dateStart + '''",
#             "plannedEndDate": "''' + dateEnd + '''"
#         }
#     ''')
#     ).execute()
#     result_json = json.loads(result.get_data(as_text=True))
    
#     assert isinstance(result, Response)
#     assert "id" in result_json

#     result_consulta = VerFligth('10').execute()
#     assert 'id' in result_consulta[0]
    
#     result_consulta = VerFligth(flight='').execute()
#     assert 'id' in result_consulta[0]

#     result_consulta = VerFligth(flight='fake').execute()
#     assert not result_consulta

#     with pytest.raises(SolicitudException) as exc_info:
#             result_consulta = VerFligth(flight='17').execute()

#     assert exc_info.type == SolicitudException
    


    
