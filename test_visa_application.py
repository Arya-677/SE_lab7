from hypothesis import given, strategies as st
from visa_application import parse_application, processing_average, payable_fee


# ---------- Fuzz tests: the functions must never crash ----------

@given(st.text() | st.none())
def test_parse_application_no_crash(s):
    try:
        parse_application(s)
    except Exception as e:
        assert False, f"parse_application crashed with: {e!r}"


@given(st.text() | st.none())
def test_processing_average_no_crash(s):
    try:
        processing_average(s)
    except Exception as e:
        assert False, f"processing_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r}"


# ---------- Extra property tests: valid input must give correct output ----------

@given(st.sampled_from(["tourist", "student", "work visa"]),
       st.integers(min_value=1, max_value=10**6))
def test_parse_application_valid(visa, entries):
    assert parse_application(f"{visa}:{entries}") == (visa.title(), entries)


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_processing_average_valid(days):
    csv = ",".join(str(d) for d in days)
    assert processing_average(csv) == sum(days) // len(days)


@given(st.integers(min_value=0, max_value=10**6),
       st.integers(min_value=0, max_value=10**6))
def test_payable_fee_never_negative(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result is not None and result >= 0
