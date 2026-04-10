import pytest
from task2 import ivp

def a():
    assert ivp("a") == False
    assert ivp("AAAAAAAAAAAAAAAAAAAAAAAAAAA") == False
    assert ivp("Abcdefg1") == True
    assert ivp("abcdefg1") == False
    assert ivp("Abcdefgh") == False

# if __name__ == "__main__":
pytest.main(["-v", __file__])