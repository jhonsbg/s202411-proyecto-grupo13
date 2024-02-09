from src.commands.crea import Create
import json
from datetime import datetime, timezone, timedelta
from flask import Response

class TestCreate():
  def test_create(self):
    current_utc_time = datetime.now(timezone.utc)
    dateStart = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    current_utc_time = datetime.now(timezone.utc) + timedelta(days=5)
    dateEnd = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    result = Create(
    json.loads('''
        {
            "flightId": "",
            "sourceAirportCode": "",
            "sourceCountry": "",
            "destinyAirportCode": "",
            "destinyCountry": "",
            "bagCost": 386,
            "plannedStartDate": "",
            "plannedEndDate": ""
        }
    ''')
    ).execute()
    
    assert isinstance(result, Response)
    assert result.status_code == 412