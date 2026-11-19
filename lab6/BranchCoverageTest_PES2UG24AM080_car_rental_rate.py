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


@pytest.mark.parametrize(
    "invalid_rentals, invalid_fee",
    [
        ("not_a_list", 10.0),
        (None, 5.0),
        ([], -1.0),
    ],
)
def test_invalid_inputs_all_branches(invalid_rentals, invalid_fee):
    with pytest.raises(ValueError, match="Invalid rental list or admin fee"):
        process_rental_fleet(invalid_rentals, invalid_fee)


def test_empty_and_unconfirmed_batches():
    assert process_rental_fleet([], 10.0) == {
        "total_revenue": 0.0,
        "status": "EMPTY_BATCH",
    }
    unconfirmed_rentals = [
        {"is_confirmed": False, "vehicle_type": "luxury", "driver_age": 22, "days": 3},
        {"is_confirmed": True, "vehicle_type": "economy", "driver_age": 25, "days": -2},
    ]
    assert process_rental_fleet(unconfirmed_rentals, 10.0) == {
        "total_revenue": 0.0,
        "status": "EMPTY_BATCH",
    }


def test_underage_ternary_and_empty_segments():
    rentals = [
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 22,
            "days": 2,
            "trip_segments": [],
        },
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 23,
            "days": 1,
            "trip_segments": [50],
        },
    ]
    # Luxury (age 22, 2 days, 0 miles): (120 * 2) + 10 + (50 * 2) = 350.0
    # SUV (age 23, 1 day, 50 miles): (70 * 1) + 10 + (50 * 0.20) + (20 * 1) = 110.0
    result = process_rental_fleet(rentals, 10.0)
    assert result == {"total_revenue": 460.0, "status": "STANDARD"}


def test_high_risk_audit_and_mileage_branches():
    rentals = [
        {"is_confirmed": True, "vehicle_type": "economy", "driver_age": 30, "days": 0},
        {
            "is_confirmed": True,
            "vehicle_type": "luxury",
            "driver_age": 20,
            "days": 1,
            "trip_segments": [-10, 350, 100],
        },
        {
            "is_confirmed": True,
            "vehicle_type": "suv",
            "driver_age": 23,
            "days": 2,
            "trip_segments": [400, 350],
        },
    ]
    # Luxury (age 20, 1 day): (120 * 1) + 10 + 250 (break on >300) + (50 * 1) = 430.0 (2 risk flags)
    # SUV (age 23, 2 days): (70 * 2) + 10 + (400 * 0.4) + (350 * 0.4) + (20 * 2) = 490.0 (2 risk flags)
    # Total risk_flags = 1 + 2 + 2 = 5 (> 4 -> HIGH_RISK_AUDIT)
    result = process_rental_fleet(rentals, 10.0)
    assert result == {"total_revenue": 920.0, "status": "HIGH_RISK_AUDIT"}


def test_check_fleet_telematics_all_branches():
    assert check_fleet_telematics([]) == "NO_DATA"
    assert check_fleet_telematics([[]]) == "SAFE"
    assert check_fleet_telematics([[80, 110, 95, 105], [70, 100]]) == "SAFE"
    assert check_fleet_telematics([[90, 105, 115]]) == "GROUND_VEHICLE"