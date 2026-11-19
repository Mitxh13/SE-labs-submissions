import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics


def test_single_economy_rental():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 2,
            "trip_segments": [100],
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result["total_revenue"] == 110.0
    assert result["status"] == "STANDARD"


def test_invalid_inputs():
    with pytest.raises(ValueError, match="Invalid rental list or admin fee"):
        process_rental_fleet("not_a_list", 10.0)


def test_unconfirmed_and_empty_batch():
    rentals = [
        {
            "is_confirmed": False,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 2,
        }
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result == {"total_revenue": 0.0, "status": "EMPTY_BATCH"}


def test_vehicle_types_and_high_risk_audit():
    rentals = [
        {"is_confirmed": True, "vehicle_type": "economy", "driver_age": 30, "days": 0},
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 20,
            "days": 1,
            "trip_segments": [-10, 350],
        },
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 28,
            "days": 2,
            "trip_segments": [400, 350],
        },
    ]
    result = process_rental_fleet(rentals, 10.0)
    assert result == {"total_revenue": 880.0, "status": "HIGH_RISK_AUDIT"}


def test_telematics_all_lines():
    assert check_fleet_telematics([]) == "NO_DATA"
    assert check_fleet_telematics([[80, 110, 90]]) == "SAFE"
    assert check_fleet_telematics([[105, 115]]) == "GROUND_VEHICLE"