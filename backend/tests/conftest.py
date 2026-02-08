import pytest
import os
from typing import Dict, Any, List
from unittest.mock import MagicMock

# Set DRY_RUN to true for tests by default to avoid real DB calls
os.environ["DRY_RUN"] = "true"

@pytest.fixture
def mock_supabase_client(mocker):
    """Mocks the Supabase client."""
    mock_client = MagicMock()
    # Mock the chain: supabase.table('...').select('...').execute()
    mock_table = MagicMock()
    mock_select = MagicMock()
    mock_execute = MagicMock()

    mock_client.table.return_value = mock_table
    mock_table.select.return_value = mock_select
    mock_table.insert.return_value = mock_select # insert also returns query builder
    mock_select.eq.return_value = mock_select
    mock_select.execute.return_value = mock_execute

    # Default response
    mock_execute.data = []

    return mock_client

@pytest.fixture
def sample_fleet_data() -> List[Dict[str, Any]]:
    return [
        {
            "id": "fleet-123",
            "company_id": "comp-1",
            "vehicle_type": "Tautliner",
            "capacity_tons": 24.0,
            "current_location_lat": 52.52,
            "current_location_lng": 13.40,
            "status": "IDLE"
        }
    ]

@pytest.fixture
def sample_load_data() -> List[Dict[str, Any]]:
    return [
        {
            "id": "load-456",
            "company_id": "comp-2",
            "origin_lat": 48.85,
            "origin_lng": 2.35,
            "destination_lat": 52.52,
            "destination_lng": 13.40,
            "weight_tons": 20.0,
            "deadline": "2023-12-31T23:59:59",
            "status": "PENDING",
            "price_offered": 1500.0
        }
    ]
