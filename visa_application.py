import math


def parse_application(text):
    """Parse 'visa_type:entries' (e.g. 'tourist:2') into ('Tourist', 2).

    Returns None for any invalid input instead of raising.
    """
    if not isinstance(text, str):
        return None

    parts = text.split(':')
    if len(parts) != 2:
        return None

    visa, entries = parts[0].strip(), parts[1].strip()
    if not visa:
        return None

    try:
        entries = int(entries)
    except ValueError:  # non-numeric, empty, or absurdly long digit string
        return None

    if entries < 1:  # a visa must allow at least one entry
        return None

    return visa.title(), entries


def processing_average(days_csv):
    """Average (floor) of comma-separated processing days, e.g. '5,10,21' -> 12.

    Returns None for any invalid input instead of raising.
    """
    if not isinstance(days_csv, str):
        return None

    values = []
    for part in days_csv.split(','):
        try:
            days = int(part.strip())
        except ValueError:  # empty element, letters, huge digit string
            return None
        if days < 0:  # negative processing time makes no sense
            return None
        values.append(days)

    if not values:
        return None

    return sum(values) // len(values)


def payable_fee(text):
    """Compute 'fee|discount' -> fee * 1.18 (GST) - discount, never below 0.

    Returns None for any invalid input instead of raising.
    """
    if not isinstance(text, str):
        return None

    parts = text.split('|')
    if len(parts) != 2:
        return None

    try:
        fee = float(parts[0])
        discount = float(parts[1])
    except ValueError:
        return None

    # reject nan / inf (float() happily parses 'nan', 'inf', '1e999')
    if not (math.isfinite(fee) and math.isfinite(discount)):
        return None

    if fee < 0 or discount < 0:
        return None

    total = fee * 1.18 - discount
    if not math.isfinite(total):  # fee * 1.18 can overflow to inf
        return None

    return max(total, 0)


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    if result is None:
        print("Invalid input. Expected format -> visa_type:entries (entries >= 1)")
    else:
        print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    if result is None:
        print("Invalid input. Expected format -> comma-separated non-negative integers")
    else:
        print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    if result is None:
        print("Invalid input. Expected format -> fee|discount (non-negative numbers)")
    else:
        print("Payable Fee:", result)


if __name__ == "__main__":
    main()
