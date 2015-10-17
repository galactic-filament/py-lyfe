from app import arithmetic


def test_subtract():
    assert arithmetic.subtract(4, 2) == 2


def test_add():
    assert arithmetic.add(2, 2) == 4
