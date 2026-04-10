import pytest
from task1 import calculate_discount

def test_calculate_discount():
    assert calculate_discount(500) == 500
    assert calculate_discount(1500) == 1425.0
    assert calculate_discount(6000) == 5400.0
    assert calculate_discount(12000) == 10200.0

if __name__ == "__main__":   
    pytest.main()