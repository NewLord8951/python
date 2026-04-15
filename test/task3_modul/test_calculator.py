import pytest
from calculator import Calculator

def test_():
    c = Calculator()
    assert c.add(1, 1) == 2
    assert c.subtract(1, 2) == -1
    assert c.multiply(2, 2) == 4
    assert c.divide(8, 2) == 4
    assert c.power(10, 5) == 100000

if __name__ == "__main__":   
    pytest.main()