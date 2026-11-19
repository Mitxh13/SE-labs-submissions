"""Point-of-sale script: totals carts, applies promo codes, logs receipts."""
import operator
import re

PRICE_LIST = {"pen": 10, "notebook": 45, "bag": 799, "bottle": 150}
STOCK = {name: 0 for name in PRICE_LIST}
STATE = {"sales_total": 0.0, "receipt_lines": []}
PROMO_PATTERN = re.compile(r"^\s*total\s*([*+/-])\s*(\d+(?:\.\d+)?)\s*$")
PROMO_OPERATORS = {
    "*": operator.mul,
    "+": operator.add,
    "-": operator.sub,
    "/": operator.truediv,
}


def process_checkout(cart_items, tax_rate=0.05, receipts=None):
    """Return the taxed total for cart_items, a list of (name, qty) pairs.

    Raises ValueError for unknown items, bad quantities or a bad tax rate,
    so a faulty bill is rejected instead of silently mis-totalled.
    """
    if receipts is None:
        receipts = []
    if not 0 <= tax_rate <= 1:
        raise ValueError(f"Invalid tax rate: {tax_rate}")
    subtotal = 0
    for name, qty in cart_items:
        if name not in PRICE_LIST:
            raise ValueError(f"Unknown item: {name}")
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError(f"Invalid quantity for {name}: {qty!r}")
        subtotal += PRICE_LIST[name] * qty
    total = subtotal * (1 + tax_rate)
    receipts.append(total)
    STATE["sales_total"] += total
    number = len(STATE["receipt_lines"]) + 1
    STATE["receipt_lines"].append(
        f"Receipt #{number:04d} total={total:.2f}"
    )
    return total


def apply_promo_code(code_str):
    """Apply a promo like 'total * 0.9' or 'total - 50' to the sales total.

    Only 'total <operator> <number>' is accepted; nothing is evaluated.
    """
    match = PROMO_PATTERN.match(code_str)
    if match is None:
        raise ValueError(f"Invalid promo code: {code_str!r}")
    symbol, value = match.group(1), float(match.group(2))
    if symbol == "/" and value == 0:
        raise ValueError("Cannot divide by zero")
    return PROMO_OPERATORS[symbol](STATE["sales_total"], value)


def update_stock(item, qty):
    """Add qty units of item to stock. Raises ValueError for unknown items."""
    if item not in STOCK:
        raise ValueError(f"Unknown item: {item}")
    STOCK[item] += qty
    print("Stock updated for", item, "by", qty)


def save_receipt_log(file="pos_log.txt"):
    """Append all receipt lines to the log file."""
    with open(file, "a", encoding="utf-8") as log_file:
        for line in STATE["receipt_lines"]:
            log_file.write(line + "\n")


def print_sales():
    """Print the running sales total."""
    print(f"Sales so far: {STATE['sales_total']:.2f}")


def main():
    """Run the demo bills, promo codes and receipt logging."""
    bills = [
        ("Bill 1", [("pen", 3), ("notebook", 2)], 0.05),
        ("Bill 2", [("bag", 1), ("laptop", 1)], 0.05),
        ("Bill 3", [("bottle", -4)], 0.05),
        ("Bill 4", [("pen", "2")], -1),
    ]
    for label, cart, rate in bills:
        try:
            print(f"{label}: {process_checkout(cart, tax_rate=rate):.2f}")
        except ValueError as err:
            print(f"{label} rejected: {err}")
    try:
        update_stock("laptop", 5)
    except ValueError as err:
        print("Stock error:", err)
    print(f"After promo: {apply_promo_code('total * 0.9'):.2f}")
    code = input("Enter promo code (e.g. total - 50): ") or "total - 50"
    try:
        print(f"After your promo: {apply_promo_code(code):.2f}")
    except ValueError as err:
        print("Promo rejected:", err)
    save_receipt_log()
    print_sales()


if __name__ == "__main__":
    main()