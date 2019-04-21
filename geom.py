__license__ = "MIT"
__docformat__ = 'reStructuredText'

import numbers
import math

"""Error tolerance used to compare floating points"""
eps = 0.0001

def set_tolerance(epsilon):
    """Set the error tolerance for which to compare floating point numbers.

    `TypeError` is raised if `epsilon` isn't numeric. `ValueError` is raised if
    `epsilon` isn't positive.
    """
    if not isinstance(epsilon, numbers.Number):
        raise TypeError("epsilon must be a positive number")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    eps = epsilon

def is_numeric(N):
    """Determine if `N` is numeric.

    `N` may be a single value or a collection.
    """
    if '__iter__' in dir(N):
        return False not in [isinstance(n, numbers.Number) for n in N]
    else:
        return isinstance(N, numbers.Number)

class Vector(object):
    """A Vector represents a mathematical vector for any dimension.

    **Overloaded Operations**

    | `len(v)` gives the dimension of the vector `v`
    | `abs(v)` gives the magnitude of the vector `v`
    | `~v` gives the normalized version of the vector `v`
    | `-v` gives the a vector in the opposite direction but same magnitude as `v`
    | `v[i]` gives the vector component in the ith dimension.
    | `a == b` compare two vectors for equality
    | `a + b` adds two vectors together
    | `a - b` subtracts the vector `b` from the vector `a`
    | `a * m` multiplies all components of the vector `a` by a scalar `m`
    | `a / m` divides all components of the vector `a` by a non-zero scalar `m`
    | `a * b` computes the cross product of the 3D vector `a` with the 3D vector `b`
    | `a @ b` computes the dot product of the the vector `a` and the vector `b`

    For binary operations, as long as one of the arguments is a `geom.Vector`,
    the other argument may be any form of numeric collection of the same
    dimension.
    """
    __slots__ = '_components'

    def __init__(self, components):
        """Create a vector from `components`

        `components` should be a collection of numeric values. Initializing
        a `Vector` with a collection of non-numeric values will raise a
        `ValueError.`
        """
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
        return False not in [abs(a-b) < eps for a, b in zip(self, other)]

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
        """The x-component of a vector. Equivalent to `v[0]`"""
        return self[0]
    @x.setter
    def x(self, other):
        self[0] = other

    @property
    def y(self):
        """The y-component of a vector. Equivalent to `v[1]`"""
        return self[1]
    @y.setter
    def y(self, value):
        self[1] = value

    @property
    def z(self):
        """The z-component of a vector. Equivalent to `v[1]`"""
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
