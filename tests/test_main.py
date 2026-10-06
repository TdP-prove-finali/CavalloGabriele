import pytest

from main import calcolo_esempio

def test_calcolo_esempio():
    with pytest.raises(ZeroDivisionError):
        calcolo_esempio(2, 0)