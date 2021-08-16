import geom
import pytest
import math

def test_is_numeric():
    assert(geom.is_numeric(3))
    assert(not geom.is_numeric('3'))
    assert(geom.is_numeric((1, 2, 3)))
    assert(geom.is_numeric([1.0, 2, 3.0012]))
    assert(not geom.is_numeric(('1', 2, 3.0)))
    assert(geom.is_numeric({1.0, 2.0, 3.0}))
    assert(not geom.is_numeric(True))

def test_vecinit():
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

def test_vecgetitem():
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

    EPSILON = 10 ** -6
    for c, e, m in zip(C, E, M):
        v = geom.Vector(c)
        mv = geom.Vector(c)
        mv.mulBy(m)

        diff = m*v - e
        assert diff.magSq() < EPSILON

        diff = v*m - e
        assert diff.magSq() < EPSILON

        diff = v.mul(m) - e
        assert diff.magSq() < EPSILON

        dif = mv - e
        assert diff.magSq() < EPSILON

    E = ((0,), (1.0,), (-6, 9), (-0.5, -0.375, -0.25))
    D = (1, 133333, -0.5, 4)
    for c, e, d in zip(C, E, D):
        v = geom.Vector(c)
        dv = geom.Vector(c)
        dv.divBy(d)

        diff = (v/d) - e
        assert diff.magSq() < EPSILON

        diff = v.div(d) - e
        assert diff.magSq() < EPSILON

        diff = dv - e
        assert diff.magSq() < EPSILON

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

def test_veccross():
    A = ((0, 0, 0), (1.0, 0, 0), (-300000, 20003, -0.020012))
    b = (3, 4, 5)
    expected = ((0, 0, 0), (0, -5.0, 4.0), (100015.08005, 1499999.939964,
                                            -1260009))

    EPSILON = 0.001
    for a, e in zip(A, expected):
        av = geom.Vector(a);
        ev = geom.Vector(e);

        diff = av*b - ev
        assert diff.magSq() < EPSILON

        diff = av.cross(b) - ev
        assert diff.magSq() < EPSILON

    bv = geom.Vector(b)
    assert(bv*A[1] != A[1]*bv)

    BT = ((True, True, 1.0), False, ("3.0", 4.2, 12), "{3.3, 1.0 5.9}",
          ((3, 4), (5, 6), (7, 8)))
    tests = ("{0} * {1}", "{1} * {0}", "{0}.cross({1})")
    for bt in BT:
        for test in tests:
            with pytest.raises(TypeError):
                eval(test.format('bv', 'bt'))

    BL = ((1,), (1, 2), (1, 2, 3, 4))
    for bl in BL:
        for test in tests:
            with pytest.raises(ValueError):
                eval(test.format('bv', 'bl'))

    BL2 = ((2,), (3, 4), (5 ,6, 7, 8))
    for bl, bl2 in zip(BL, BL2):
        blv = geom.Vector(bl)
        for test in tests:
            with pytest.raises(ValueError):
                eval(test.format('blv', 'bl2'))

def test_circinit():
    centers = ((0, 0), (-0.0001, -0.00023), (3002.0002, -4003.2093))
    radii = (0, 0.00032, 5.0021)
    for p, r in zip(centers, radii):
        c1 = object.__new__(geom.Circle)
        c1._center = geom.Vector(p)
        c1._radius = r
        c2 = geom.Circle(p, r)
        assert(c1.center == c2.center)
        assert(abs(c1.radius-c2.radius) < geom.EPSILON)

    with pytest.raises(TypeError):
        geom.Circle('{1, 2}', 3)

    class Test(object):
        __slots__ = ['components']
        def __iter__(self):
            yield from self.components

    a = object.__new__(Test)
    a.components = [1, 2]
    with pytest.raises(AttributeError):
        geom.Circle(a, 3.00002)

    with pytest.raises(ValueError):
        geom.Circle((1,), 30000)
    with pytest.raises(ValueError):
        geom.Circle((1, 1, 1), 0.0001)

    with pytest.raises(TypeError):
        geom.Circle((1, 2), '3')

    with pytest.raises(ValueError):
        geom.Circle((20, 30), -39)

def test_circarea():
    centers = ((0, 0), (-1.0, 1.0), (10000, 0.000001), (-7892822, 1902383))
    radii = (33.19, 0, 0.02003, 78892)
    areas = (0, 16*math.pi, 0.000025, 3423423)
    eas = (3460.7033830094, 0, 0.0012604098, 19553108257.54975484)
    ers = (0, 4, 0.00282095, 1043.8914625)
    for center, r, area, ea, er in zip(centers, radii, areas, eas, ers):
        c = geom.Circle(center, r)
        assert(abs(c.area-ea) < geom.EPSILON)
        c.area = area
        assert(abs(c.radius-er) < geom.EPSILON)
    c = geom.Circle((0,0),1)
    tests = (True, "3.4", (5, 4))
    for test in tests:
        with pytest.raises(TypeError):
            c.area = test
    with pytest.raises(ValueError):
        c.area = -23.4123

def test_circumference():
    centers = ((0, 0), (-1.0, -1.0), (-1000000, 1000000), (0.000032, 0.02302))
    radii = (.5/math.pi, 0, 203023, 15.76231)
    circumferences = (0, 20*math.pi, 0.016, 2910292)
    ecs = (1, 0, 1275631.13061952, 99.037514599)
    ers = (0, 10, 0.00254648, 463187.3576408)
    for p, r, c, ec, er in zip(centers, radii, circumferences, ecs, ers):
        circle = geom.Circle(p, r)
        assert(abs(circle.circumference-ec) < geom.EPSILON)
        circle.circumference = c
        assert(abs(circle.radius-er) < geom.EPSILON)
    c = geom.Circle((0,0),1)
    tests = (False, '33232', (5.0, 92.1, 2329))
    for test in tests:
        with pytest.raises(TypeError):
            c.circumference = test
    with pytest.raises(ValueError):
        c.circumference = -1

def test_circscale():
    centers = ((0, 0), (1.0 , 1), (-20391023, 23090233), (0.0203, 0.00312))
    radii = (1, 0, 0.0549, 102930201)
    m = 33.12
    AM = (33.12, 204124, 204124, 0.001203)
    er1 = 33.12
    er2 = 5.27121172
    er3 = 3.24690983
    ER4 = (33.12, 0, 1.818288, 3409048257.12)
    ER5 = (5.754997828, 0, 24.80386618, 3570060.98159599823)
    for p, r, er4, er5, am in zip(centers, radii, ER4, ER5, AM):
        circle = geom.Circle(p, r)
        test = circle.scaled_to(m)
        assert(abs(test.radius-er1) < geom.EPSILON)
        assert(abs(circle.radius-r) < geom.EPSILON)
        test = circle.scaled_to(m, 'circumference')
        assert(abs(test.radius-er2) < geom.EPSILON)
        test = circle.scaled_to(m, 'area')
        assert(abs(test.radius-er3) < geom.EPSILON)
        test = circle.scaled_by(m)
        assert(abs(test.radius-er4) < geom.EPSILON)
        test = circle.scaled_by(am, 'area')
        assert(abs(test.radius-er5) < geom.EPSILON)

    circle = geom.Circle((0,0), 1)
    gat = ('radius', 'circumference', 'area')
    bmt = ((3, 4, 5), False, '3.43')
    for m, a in zip(bmt, gat):
        with pytest.raises(TypeError):
            circle.scaled_to(m, attr=a)
        with pytest.raises(ValueError):
            circle.scaled_to(-2.3)

    gab = ('radius', 'area')
    bmt = (geom.Circle((0,0), 1), range(1,2))
    for m, a in zip(bmt, gab):
        with pytest.raises(TypeError):
            circle.scaled_by(m, attr=a)
        with pytest.raises(ValueError):
            circle.scaled_by(-3003202)

    gm = (13.3, 0.005, 302393, 0)
    batt = (True, 0.232, geom.Circle((0,0),1))
    batv = ('spaghetti', 'r', 'a')
    for m, at, av in zip(gm, batt, batv):
        with pytest.raises(TypeError):
            circle.scaled_to(m, attr=at)
        with pytest.raises(ValueError):
            circle.scaled_to(m, attr=av)

    gm = (0.00232, 9000212.0302, 23)
    babt = (range(1000), False, 2003)
    babv = ('circumference', 'r', 'pasta')
    for m, at, av in zip(gm, babt, babv):
        with pytest.raises(TypeError):
            circle.scaled_by(m, attr=at)
        with pytest.raises(ValueError):
            circle.scaled_by(m, attr=av)

def test_circmoved():
    center = (23.4, -99)
    circle = geom.Circle(center, 34.09)

    posv = ((0, 0), (-12003032, 0.00012303))
    for pos in posv:
        c = circle.moved_to(pos)
        assert(c.center == pos)

    vecv = ([0, 0], (1, 0), {0, -203}, geom.Vector((0.3213, 45.23)))
    posv = (center, (24.4, -99), (23.4, -302), (23.7213, -53.77))
    for vec, pos in zip(vecv, posv):
        c = circle.moved_by(vec)
        assert(c.center == pos)

    vecv = (33, 1.203, ('2', 3, 0.4), True, '(3, 4, 5)', geom.Circle((1,2),3))
    for vec in vecv:
        with pytest.raises(TypeError):
            circle.moved_to(vec)
        with pytest.raises(TypeError):
            circle.moved_by(vec)

    vecv = ((1.9,), (-43,), (203, -804.10, 0))
    for vec in vecv:
        with pytest.raises(ValueError):
            circle.moved_to(vec)
        with pytest.raises(ValueError):
            circle.moved_by(vec)

def test_circ_intersects():
    posv1 = ((0, 0), (0.0023, -0.0031), (5782, 8792.1), (4, 5))
    radii1 = (5, 0.00401, 33.9782, 1)
    posv2 = ((0, 0), (-60793, 20034), (5750, 8778), (5, 4))
    radii2 = (0, 64008.98293, 35, 10)
    posv3 = ((0, 5.000002), (-60793, 20034), (-5782, -8792.1), (10, 10))
    radii3 = (0.000001, 64008.98292, 33.9782, 0.5)
    for pos1, r1, pos2, r2, pos3, r3 in zip(posv1, radii1, posv2, radii2,
                                            posv3, radii3):
        c1 = geom.Circle(pos1, r1)
        c2 = geom.Circle(pos2, r2)
        c3 = geom.Circle(pos3, r3)
        assert(c1.intersects(c2))
        assert(c2.intersects(c1))
        assert(not c1.intersects(c3))
        assert(not c3.intersects(c1))

    circ = geom.Circle(posv1[0], radii1[0])
    posv4 = ((0,0), (0, 5), (4*math.cos(math.pi/6),4*math.cos(math.pi/6)),
             (1.29*math.cos(3*math.pi/8), 4.33*math.sin(3*math.pi/8)))
    for pos1, pos2 in zip(posv3, posv4):
        assert(not circ.intersects(pos1))
        assert(circ.intersects(pos2))

    tests = (((0,0), 5), 'Circle((0,0), 5)', {'center': (0,0),'radius':5})
    for test in tests:
        with pytest.raises(TypeError):
            circ.intersects(test)

