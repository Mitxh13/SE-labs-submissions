import math


def sanitize_license_plate(plate):
    if plate is None or not isinstance(plate, str):
        return ""
    plate = plate.strip()
    for ch in ['-', ' ', '_', '#']:
        plate = plate.replace(ch, '')
    return plate.upper()


def parse_trip_mileage(mileage_csv):
    if mileage_csv is None or not isinstance(mileage_csv, str) or not mileage_csv.strip():
        return []
    mileages = []
    for part in mileage_csv.split(','):
        cleaned = part.strip()
        if not cleaned:
            continue
        try:
            value = float(cleaned)
            if math.isfinite(value) and value >= 0:
                mileages.append(value)
        except ValueError:
            continue
    return mileages


def format_rental_invoice(record):
    if record is None or not isinstance(record, str) or not record.strip():
        return "Invalid rental record"
    parts = record.split(':')
    if len(parts) != 3:
        return "Invalid rental record"
    driver = parts[0].strip()
    days_str = parts[1].strip()
    category = parts[2].strip()
    if not driver or not category:
        return "Invalid rental record"
    try:
        days = int(days_str)
    except ValueError:
        return "Invalid rental record"
    if days <= 0:
        return "Invalid rental record"
    daily_rate = 50.0 if category.lower() == "suv" else 30.0
    total = days * daily_rate
    return f"Driver {driver} booked {category} for {days} days: Total ${total:.2f}"


def main():
    print("==== Running sanitize_license_plate ====")
    raw_plate = input("Enter license plate with delimiters (-, _, #): ")
    clean_plate = sanitize_license_plate(raw_plate)
    print("Sanitized Plate:", clean_plate)

    print("\n==== Running parse_trip_mileage ====")
    csv_input = input("Enter CSV of mileages (e.g. 100.5, 45.2, 80.0): ")
    mileage_list = parse_trip_mileage(csv_input)
    print("Parsed Mileage List:", mileage_list)

    print("\n==== Running format_rental_invoice ====")
    record_input = input("Enter rental record (Driver:Days:Category): ")
    invoice = format_rental_invoice(record_input)
    print("Rental Invoice:", invoice)


if __name__ == "__main__":
    main()