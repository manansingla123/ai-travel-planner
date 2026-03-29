import pytest
from tools.arthamatic_op_tool import multiply, add

def test_multiply():
    assert multiply.invoke({"a": 3, "b": 4}) == 12
    assert multiply.invoke({"a": -1, "b": 5}) == -5
    assert multiply.invoke({"a": 0, "b": 100}) == 0

def test_add():
    assert add.invoke({"a": 10, "b": 20}) == 30
    assert add.invoke({"a": -5, "b": 5}) == 0
    assert add.invoke({"a": 0, "b": 0}) == 0

# You can add more tool tests here, e.g., mocking API calls for weather/currency
