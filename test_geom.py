import geom
import pytest

def test_epsilon():
    assert(abs(geom.eps - 0.0001) < 0.0001)
    geom.set_tolerance(0.01)
    assert(abs(geom.eps - 0.01) < 0.01)
    with pytest.raises(TypeError):
        geom.set_tolerance('0.001')
    with pytest.raises(ValueError):
        geom.set_tolerance(0)
    with pytest.raises(ValueError):
        geom.set_tolerance(-1)

def test_is_numeric():
    assert(geom.is_numeric(3))
    assert(not geom.is_numeric('3'))
    assert(geom.is_numeric((1, 2, 3)))
    assert(geom.is_numeric([1.0, 2, 3.0012]))
    assert(not geom.is_numeric(('1', 2, 3.0)))
    assert(geom.is_numeric({1.0, 2.0, 3.0}))

def test_new_vector():
    cases = [(1, 2, 3), [1.0, 2.0, 3.0], {1, 2, 3.0}, range(1,4)]
    expected = [1, 2, 3]
    for v in cases:
        assert geom.Vector(v)._components == expected

def test_veclen():
    cases = [(), (0,), (0,0,0,0,0)]
    expected = [0, 1, 5]
    for v, n in zip(cases, expected):
        assert(len(geom.Vector(v)) == n)

def test_getitem():
    I = (0, 1, 2, 19)
    A = ('x', 'y', 'z')
    V = [[2*i for i in range(n)] for n in range(4)]
    V.append([3*i for i in range(20)])
    expected = {'index': ((), (0,), (0, 2), (0, 2, 4), (0, 3, 6, 57)),
                'attr': ((), (0,), (0, 2), (0, 2, 4), (0, 3, 6))}

    for i, components in enumerate(V):
        v = geom.Vector(components)
        for j, index in enumerate(I):
            if j >= len(expected['index'][i]):
                with pytest.raises(IndexError):
                    v[index]
            else:
                assert(v[index] == expected['index'][i][j])
                
        for j, attr in enumerate(A):
            if j >= len(expected['attr'][i]):
                with pytest.raises(IndexError):
                    getattr(v, attr)
            else:
                assert(getattr(v, attr) == expected['attr'][i][j])

def test_mag():
    cases = ((0,), (1,), (3, 4), (1.0, 1.0), (0.1, 4.0, 79.0))
    expected = (0, 1, 5, 2**0.5, 79.1013)
    for components, e in zip(cases, expected):
        v = geom.Vector(components)
        assert(abs(v)-e < 0.0001)
        assert(v.mag()-e < 0.0001)
        assert(v.magSq()-(e**2) < 0.0001)
