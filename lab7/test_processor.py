import math
from hypothesis import given, strategies as st
from processor import sanitize_license_plate, parse_trip_mileage, format_rental_invoice


@given(st.text() | st.none())
def test_sanitize_license_plate_no_crash(s):
    try:
        result = sanitize_license_plate(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"sanitize_license_plate crashed with: {e}"


@given(st.text() | st.none())
def test_parse_trip_mileage_safe(s):
    try:
        result = parse_trip_mileage(s)
        assert isinstance(result, list)
        assert all(isinstance(x, float) and math.isfinite(x) and x >= 0 for x in result)
    except Exception as e:
        assert False, f"parse_trip_mileage crashed with: {e}"


@given(st.text() | st.none())
def test_format_rental_invoice_safe(s):
    try:
        result = format_rental_invoice(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"format_rental_invoice crashed with: {e}"