from src.run import makeOutput
from main import main
import pytest
from src.exceptions import CustomError
from unittest import TestCase


def test_good_expr():
    main("* * * * * *")


def test_too_short_expr():
    with pytest.raises(CustomError) as excinfo:
        main("* * * * *")
    assert str(excinfo.value) == "ERROR: Invalid length of cron expression"


def test_make_output_1():
    output = makeOutput(["1", "1", "1", "1", "1", "/test/command"])

    expected_output = {
        "minute": "1",
        "hour": "1",
        "day of month": "1",
        "month": "1",
        "day of week": "1",
        "command": "/test/command",
    }

    TestCase().assertDictEqual(expected_output, output)


# ExprParser parse related tests
def test_minute_comma():
    output = makeOutput(["1,2,3,4", "*", "*", "*", "*", "/folder/file"])
    expected_output = {
        "minute": "1 2 3 4",
    }

    TestCase().assertEqual(expected_output["minute"], output["minute"])


def test_minute_invalid_comma():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["101,2", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid time format"


def test_minute_range():
    output = makeOutput(["1-5", "*", "*", "*", "*", "/folder/file"])
    expected_output = {
        "minute": "1 2 3 4 5",
    }

    TestCase().assertEqual(expected_output["minute"], output["minute"])


def test_minute_invalid_number():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["60", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid time format"


def test_minute_invalid_range():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["6-5", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid range in expression"


def test_minute_invalid_time_format():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["100-123", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid time format"


def test_star_parser_day_of_week():
    output = makeOutput(["*", "*", "*", "*", "*", "/folder/file"])
    expected_output = {
        "day of week": "1 2 3 4 5 6 7",
    }
    TestCase().assertEqual(
        expected_output["day of week"], output["day of week"]
    )


def test_star_parser_month():
    output = makeOutput(["*", "*", "*", "*", "*", "/folder/file"])
    expected_output = {
        "month": "1 2 3 4 5 6 7 8 9 10 11 12",
    }
    TestCase().assertEqual(expected_output["month"], output["month"])


def test_increment_parser_minute():
    output = makeOutput(["*/15", "*", "*", "*", "*", "/folder/file"])
    expected_output = {"minute": "0 15 30 45"}
    TestCase().assertEqual(expected_output["minute"], output["minute"])


def test_increment_start_greater_than_max():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["60/15", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid range in expression"


# ExprParser isValid related tests
def test_invalid_increment_expr_1():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["*/a", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid expression format"


def test_invalid_increment_expr_2():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["15/a", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid expression format"


def test_invalid_range_expr_1():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["10-x", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid expression format"


def test_invalid_range_expr_2():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["x-1", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid expression format"


def test_invalid_comma_expr_1():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["1,2,3,x,5", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid expression format"


def test_invalid_star_expr_1():
    with pytest.raises(CustomError) as excinfo:
        makeOutput(["**", "*", "*", "*", "*" "/folder/file"])
    assert str(excinfo.value) == "ERROR: Invalid expression format"
