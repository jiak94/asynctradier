from asynctradier.utils.common import (
    build_option_symbol,
    is_valid_expiration_date,
    is_valid_option_type,
)


def test_build_option_symbol():
    symbol = build_option_symbol(
        symbol="SPY",
        expiration_date="2021-01-15",
        strike=300.0,
        option_type="CALL",
    )
    assert symbol == "SPY210115C00300000"


def test_is_valid_expiration_date():
    d = "2021-01-15"
    assert is_valid_expiration_date(d) is True
    d = "2021-1-15"
    assert is_valid_expiration_date(d) is False
    d = "2021-01-5"
    assert is_valid_expiration_date(d) is False
    d = "2021-1-5"
    assert is_valid_expiration_date(d) is False
    d = "2021-01-05"
    assert is_valid_expiration_date(d) is True


def test_is_valid_option_type():
    assert is_valid_option_type("CALL") is True
    assert is_valid_option_type("PUT") is True
    assert is_valid_option_type("call") is True
    assert is_valid_option_type("put") is True
    assert is_valid_option_type("C") is False
    assert is_valid_option_type("P") is False
    assert is_valid_option_type("c") is False
    assert is_valid_option_type("p") is False
