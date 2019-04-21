import numbers
import math

EPS = 0.0001

def set_tolerance(eps):
    """Set the error tolerance for which to compare floating point numbers.
    
    Raises """
    if not isinstance(eps, numbers.Number):
        raise TypeError("epsilon must be a positive number")
    if eps <= 0:
        raise ValueError("epsilon must be positive")
    EPS = eps

def is_numeric(N):
    """Determine if N is numeric.

    N -- an object or a collection of objects
    """
    if '__iter__' in dir(N):
        return False not in [isinstance(n, numbers.Number) for n in N]
    else:
        return isinstance(N, numbers.Number)

class Vector(object):
    __slots__ = '_components'

    def __init__(self, components):
        if not is_numeric(components):
            raise ValueError("components must be numeric values")
        self._components = list(components)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, i):
        if i > len(self):
            raise IndexError("Vector has less than %d dimensions" % (i+1))
        return self._components[i]

    def __setitem__(self, i, value):
        if not isinstance(value, numbers.Number):
            raise TypeError("Vector components must be numeric")
        if i > len(self):
            raise IndexError("Vector has less than %d dimensions" % (i+1))
        self._components[i] = value

    def __eq__(self, other):
        if len(self) != len(other):
            raise ValueError("Vectors of different dimensions cannot be " +
                             "compared")
        return False not in [abs(a-b) < EPS for a, b in zip(self, other)]

    def __add__(self, other):
        if not is_numeric(other):
            raise ValueError("Added vector must have numeric components")
        if len(other) != len(self):
            raise ValueError("Cannot add vectors of two different dimensions")
        return Vector([a + b for a, b in zip(self, other)])

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not is_numeric(other):
            raise ValueError("Subtracted vector must have numeric components")
        if len(other) != len(self):
            raise ValueError("Cannot subtract vectors of two different " +
                             "dimensions")
        return Vector([a - b for a, b in zip(self, other)])

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not is_numeric(other):
            raise ValueError("Second argument must be numeric")
        if isinstance(other, numbers.Number):
            return Vector([other*c for c in self])
        if len(self) != 3 and len(other) != 3:
            raise ValueError("Can only perform 3D cross products")
        cross = Vector([self[2]*other[3] - self[3]*other[2],
                        self[3]*other[1] - self[1]*other[3],
                        self[1]*other[2] - self[2]*other[1]])
        return cross

    def __rmul__(self, other):
        if not is_numeric(other):
            raise ValueError("Second argument must be numeric")
        if isinstance(other, numbers.Number):
            return self * other
        if len(self) != 3 and len(other) != 3:
            raise ValueError("Can only perform 3D cross products")
        cross = Vector([other[2]*self[3] - other[3]*self[2],
                        other[3]*self[1] - other[1]*self[3],
                        other[1]*self[2] - other[2]*self[1]])
        return cross

    def __matmul__(self, other):
        if len(self) != len(other):
            raise ValueError("Cannot perform dot product on vectors of two " +
                             "different dimensions")
        return sum([a*b for a, b in zip(a, b)])

    def __rmatmul__(self, other):
        return self @ other

    def __neg__(self):
        return Vector([-a for a in self])

    def __abs__(self):
        return math.sqrt(sum([a*a for a in self]))

    def __invert__(self):
        if abs(self) == 0:
            raise ValueError("Cannot normalize the zero vector")
        return self*(1/abs(self))

    @property
    def x(self):
        return self[0]
    @x.setter
    def x(self, other):
        self[0] = other

    @property
    def y(self):
        return self[1]
    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        return self[2]
    @z.setter
    def z(self, value):
        self[2] = value

    def magSq(self):
        return sum([a*a for a in self])

    def mag(self):
        return abs(self)

    def addOn(self, other):
        if not is_numeric(other):
            raise ValueError("Added vector must be numeric")
        if len(other) != len(self):
            raise ValueError("Added vector must have same dimensions")
        for i in range(len(self)):
            self[i] += other[i]

    def takeAway(self, other):
        if not is_numeric(other):
            raise ValueError("Added vector must be numeric")
        if len(other) != len(self):
            raise ValueError("Added vector must have same dimensions")
        for i in range(len(self)):
            self[i] -= other[i]

    def mulBy(self, m):
        if not isinstance(m, numbers.Number):
            raise TypeError("Vectors can only be multiplied by scalars")
        for i in range(len(self)):
            self[i] *= m

    def divBy(self, m):
        if not isinstance(m, numbers.Number):
            raise TypeError("Vectors can only be divided by scalars")
        for i in range(len(self)):
            self[i] /= m

    def normalize(self):
        if abs(self) == 0:
            raise ValueError("Cannot normalize the zero vector")
        self.divBy(abs(self))

    def dot(self, other):
        return self @ other

    def cross(self, other):
        return self * other

    def norm(self):
        return ~self
