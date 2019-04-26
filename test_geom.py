import geom
import pytest

def test_epsilon():
    assert(abs(geom.eps - 0.0001) < 0.0001)
    geom.set_tolerance(0.01)
    assert(abs(geom.eps - 0.01) < 0.00001)
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
    assert(not geom.is_numeric(True))

def test_new_vector():
    vc = object.__new__(geom.Vector)
    vc._components = [1, 2, 3]
    cases = [(1, 2, 3), [1.0, 2.0, 3.0], {1, 2, 3.0}, range(1,4), vc]
    expected = [1, 2, 3]
    for v in cases:
        assert(geom.Vector(v)._components == expected)
    with pytest.raises(ValueError):
        geom.Vector(())
    with pytest.raises(TypeError):
        geom.Vector(('1', 2.0, 3))
    with pytest.raises(TypeError):
        geom.Vector(1)

def test_veclen():
    cases = ((0,), (0,0,0,0,0))
    expected = (1, 5)
    for v, n in zip(cases, expected):
        assert(len(geom.Vector(v)) == n)

def test_vec_getitem():
    I = (0, 1, 2, 19)
    A = ('x', 'y', 'z')
    V = [[2*i for i in range(n)] for n in range(1,4)]
    V.append([3*i for i in range(20)])
    expected = {'index': ((0,), (0, 2), (0, 2, 4), (0, 3, 6, 57)),
                'attr': ((0,), (0, 2), (0, 2, 4), (0, 3, 6))}

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

def test_vecmag():
    cases = ((0,), (1,), (3, 4), (1.0, 1.0), (0.1, 4.0, 79.0))
    expected = (0, 1, 5, 2**0.5, 79.1013)
    for components, e in zip(cases, expected):
        v = geom.Vector(components)
        assert(abs(v)-e < 0.0001)
        assert(v.mag()-e < 0.0001)
        assert(v.magSq()-(e**2) < 0.0001)

def test_vecnorm():
    cases = ((1,), (3, 4), (0.1, 10, 100))
    for components in cases:
        v = geom.Vector(components)
        n1 = ~v
        n2 = v.norm()
        n3 = geom.Vector(components)
        n3.normalize()
        for n in (n1, n2, n3):
            assert n is not None
            assert(abs(abs(n)-1.0) < 0.0001)
            m = v.x/n.x
            assert(m > 0)
            assert(False not in [abs(m-i/j) < 0.0001 for i, j in zip(v, n)])

    with pytest.raises(ValueError):
        ~geom.Vector((0, 0))

def test_veceq():
    A = ((0,), (3.33334,), (-12000, -57.42))
    B = ((0,), (3.33333,), (-12000, -57.42))
    for a, b in zip(A, B):
        assert(geom.Vector(a) == geom.Vector(b))
    geom.set_tolerance(0.000001)
    A = ((-10000, 10000), (3.33334,), (2, 3, 4))
    B = ((10000, -10000), (3.33333,), (3, 3, 3))
    for a, b in zip(A, B):
        assert(geom.Vector(a) != geom.Vector(b))

def test_vecneg():
    cases = ((0.0,), (1,), (-2, -3.0), (34.5, -22, 130))
    expected = ((0.0,), (-1,), (2, 3.0), (-34.5, 22, -130))
    for cv, ce in zip(cases, expected):
        v = geom.Vector(cv)
        e = geom.Vector(ce)
        assert(e == -v)

def test_vecadd():
    A = ((0,), (1.34,), (-4, 6), (1900, 2000, 3000))
    B = ((0,), (3,), (6, -4), (0.01, 1.01, 0.5))
    esum = ((0,), (4.34,), (2, 2), (1900.01, 2001.01, 3000.5))
    edifa = ((0,), (-1.66,), (-10, 10), (1899.99, 1998.99, 2999.5))
    edifb = ((0,), (1.66,), (10, -10), (-1899.99, -1998.99, -2999.5))
    for ca, cb, ces, ceda, cedb in zip(A, B, esum, edifa, edifb):
        a = geom.Vector(ca)
        b = geom.Vector(cb)

        ms1 = geom.Vector(ca)
        ms1.addOn(cb)

        ms2 = geom.Vector(cb)
        ms2.addOn(a)

        mda1 = geom.Vector(ca)
        mda2 = geom.Vector(ca)
        mda1.takeAway(b)
        mda2.takeAway(cb)

        mdb1 = geom.Vector(cb)
        mdb2 = geom.Vector(cb)
        mdb1.takeAway(a)
        mdb2.takeAway(ca)

        es = geom.Vector(ces)
        eda = geom.Vector(ceda)
        edb = geom.Vector(cedb)

        sums = (a+b, b+a, a+cb, ca+b, a.add(b), b.add(ca), ms1, ms2)
        diffa = (a-b, a + -b, a-cb, ca-b, a.sub(b), a.sub(cb), mda1, mda2)
        diffb = (b-a, b + -a, b-ca, cb-a, b.sub(a), b.sub(ca), mdb1, mdb2)

        for s, da, db in zip(sums, diffa, diffb):
            assert(s == es)
            assert(da == eda)
            assert(db == edb)

    a = geom.Vector((1, 2))
    bt = (3, '4')
    bl = ((3, 4, 5), (), (2,))

    tests = ['a + %s', '%s + a', 'a - %s', 'a.add(%s)', 'a.sub(%s)',
             'a.addOn(%s)', 'a.takeAway(%s)']
    for test in tests:
        with pytest.raises(TypeError):
            eval(test % 'bt')
        for v in bl:
            with pytest.raises(ValueError):
                eval(test % 'v')

def test_vecmul():
    C = ((0,), (133333,), (3, -4.5), (-2.0, -1.5, -1.0))
    E = ((0,), (-266666,), (0, 0), (66.6, 49.95, 33.3))
    M = (30, -2, 0, -33.3)
    for c, e, m in zip(C, E, M):
        v = geom.Vector(c)
        mv = geom.Vector(c)
        mv.mulBy(m)
        assert(m*v == e)
        assert(v*m == e)
        assert(v.mul(m) == e)
        assert(mv == e)

    E = ((0,), (1.0,), (-6, 9), (-0.5, -0.375, -0.25))
    D = (1, 133333, -0.5, 4)
    for c, e, d in zip(C, E, D):
        v = geom.Vector(c)
        dv = geom.Vector(c)
        dv.divBy(d)
        assert(v/d == e)
        assert(v.div(d) == e)
        assert(dv == e)

    v = geom.Vector(range(1, 4))
    tests = ("v * %s", "%s * v", "v.add(%s)", "v.addOn(%s)",
             "v / %s", "v.div(%s)", "v.divBy(%s)")
    bad = ("'3'", 'True', 'None', (3, 4))
    for bt in bad:
        for test in tests:
            with pytest.raises(TypeError):
                eval(test % bt)

    tests = ("v / %s", "v.div(%s)", "v.divBy(%s)")
    for test in tests:
        with pytest.raises(ZeroDivisionError):
            eval(test % '0')

def test_vecdot():
    A = ((0,), (1,), (0.003, 0.004), (4123213.0, 12093201, 3298928))
    B = ((30,), (0.5,), (-0.008, 0.006), (2, 3.3, 4.01))
    expected = (0, 0.5, 0, 61382690.58)
    for a, b, e in zip(A, B, expected):
        v = geom.Vector(a);
        assert(abs((v @ b) -  e) < 0.001)
        assert(abs((b @ v) - e) < 0.001)
        assert(abs(v.dot(b) - e) < 0.001)

    A = ((1,), (1, 1), (1, 1, 1))
    BT = (("zero",), ((1, 2), (3, 4)), (True, 0, "False"))
    tests = ("{0} @ {1}", "{1} @ {0}", "{0}.dot({1})")
    for a, bt in zip(A, BT):
        av = geom.Vector(a)
        for test in tests:
            with pytest.raises(TypeError):
                eval(test.format('av', 'bt'))

    A = ((1,), (1, 1, 1))
    b = (1, 1)
    for a in A:
        av = geom.Vector(a)
        for test in tests:
            with pytest.raises(ValueError):
                eval(test.format('av', 'b'))
