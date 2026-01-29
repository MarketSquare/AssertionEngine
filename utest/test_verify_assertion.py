import pytest

import ast

from assertionengine.assertion_engine import (
    float_str_verify_assertion,
    int_str_verify_assertion,
    bool_verify_assertion,
    list_verify_assertion,
    int_dict_verify_assertion,
    AssertionOperator,
)
from robot.libraries.BuiltIn import BuiltIn


def test_float_returns_value_when_operator_none():
    assert float_str_verify_assertion(123, None, None) == 123


def test_float_numeric_operator_converts_expected_to_float_and_passes():
    result = float_str_verify_assertion(3.14, AssertionOperator["=="], "3.14")
    assert result == 3.14
    result = float_str_verify_assertion(3, AssertionOperator["=="], "3")
    assert result == 3.0


def test_float_numeric_operator_mismatch_raises_assertion_error():
    with pytest.raises(AssertionError):
        float_str_verify_assertion(3.14, AssertionOperator["=="], "2.0")


def test_float_invalid_operator_raises_value_error_float():
    with pytest.raises(ValueError):
        float_str_verify_assertion("abc", AssertionOperator["*="], "abc")


def test_int_numeric_operator_converts_expected_to_int_and_passes():
    result = int_str_verify_assertion(3, AssertionOperator["=="], "3")
    assert result == 3
    result = int_str_verify_assertion(3, AssertionOperator["=="], "3.1")
    assert result == 3
    result = int_str_verify_assertion(3.0, AssertionOperator["=="], "3")
    assert result == 3
    with pytest.raises(AssertionError) as excinfo:
        int_str_verify_assertion(3.1, AssertionOperator["=="], "4.3")
    assert "'3.1' (float) should be '4' (int)" == str(excinfo.value)
    with pytest.raises(AssertionError) as excinfo:
        int_str_verify_assertion(3, AssertionOperator["=="], "4.3")
    assert "'3' (int) should be '4' (int)" == str(excinfo.value)


def test_bool_returns_value_when_operator_none():
    assert bool_verify_assertion(True, None, None) is True


def test_bool_eq_with_truthy_expected_passes():
    assert bool_verify_assertion(True, AssertionOperator["=="], "yes") is True


def test_bool_eq_mismatch_raises_assertion_error():
    with pytest.raises(AssertionError):
        bool_verify_assertion(True, AssertionOperator["=="], False)


def test_bool_ne_operator_passes_and_returns_value():
    res = bool_verify_assertion(False, AssertionOperator["!="], "yes")
    assert res is False


def test_bool_invalid_operator_raises_value_error():
    with pytest.raises(ValueError):
        bool_verify_assertion(True, AssertionOperator["<"], "yes")


def test_list_operator_none_returns_value():
    value = [1, 2]
    assert list_verify_assertion(value, None, None) == value


def test_list_eq_operator_sorts_and_passes():
    value = [2, 1]
    res = list_verify_assertion(value, AssertionOperator["=="], [1, 2])
    assert res == [1, 2]


def test_list_ne_operator_raises_when_equal_after_sort():
    with pytest.raises(AssertionError):
        list_verify_assertion([1, 2], AssertionOperator["!="], [2, 1])


def test_int_dict_numeric_operator_applies_to_each_value():
    value = {"a": 1, "b": 2}
    res = int_dict_verify_assertion(value, AssertionOperator["=="], {"a": 1, "b": 2})
    assert res == value
