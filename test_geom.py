import geometry
import pytest

def test_epsilon():
    assert(abs(geometry.EPS - 0.0001) < 0.0001)
    geometry.set_tolerance(0.01)
    assert(abs(geometry.EPS - 0.01) < 0.01)
    with pytest.raises(TypeError):
        geometry.set_tolerance('0.001')
    with pytest.raises(ValueError):
        geometry.set_tolerance(0)
        geometry.set_tolerance(-1)

def test_is_numeric():
    assert(geometry.is_numeric(3))
    assert(not geometry.is_numeric('3'))
    assert(geometry.is_numeric((1, 2, 3)))
    assert(geometry.is_numeric([1.0, 2, 3.0012]))
    assert(not geometry.is_numeric(('1', 2, 3.0)))
    assert(geometry.is_numeric({1.0, 2.0, 3.0}))

def test_new_vector():
    cases = [(1, 2, 3), [1.0, 2.0, 3.0], {1, 2, 3.0}]
    expected = [1, 2, 3]
    for v in cases:
        assert geometry.Vector(v)._components == expected

def test_veclen():
    cases = [(), (0,), (0,0,0,0,0)]
    expected = [0, 1, 5]
    for v, n in zip(cases, expected):
        assert(len(geometry.Vector(v)) == n)
