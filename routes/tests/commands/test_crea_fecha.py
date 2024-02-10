from src.commands.crea import Create
import json
from datetime import datetime, timezone, timedelta
from flask import Response

class TestCreateFecha():
  def test_create_fecha(self):
    current_utc_time = datetime.now(timezone.utc)
    dateStart = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    current_utc_time = datetime.now(timezone.utc) - timedelta(days=5)
    dateEnd = current_utc_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    result = Create(
    json.loads('''
        {
            "flightId": "194",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LOW",
            "destinyCountry": "Inglaterra",
            "bagCost": 386,
            "plannedStartDate": "''' + dateStart + '''",
            "plannedEndDate": "''' + dateEnd + '''"
        }
    ''')
    ).execute()
    
    assert isinstance(result, Response)
    assert result.status_code == 412