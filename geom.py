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
    global eps
    if not isinstance(epsilon, numbers.Number) or isinstance(epsilon, bool):
        raise TypeError("epsilon must be a positive number")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    eps = epsilon

def is_numeric(N):
    """Determine if `N` is numeric.

    `N` may be a single value or a collection.
    """
    def is_num(n):
        return isinstance(n, numbers.Number) and (not isinstance(n, bool))
    if '__iter__' in dir(N):
        return False not in [is_num(n) for n in N]
    else:
        return is_num(N)

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
    | `a * b` computes the cross product of the `a` with `b`, where `a` and `b`
    |           are numeric collections in R3.
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
        `TypeError.` ValueError is raised if Vector is initialized with no
        components.
        """
        if not hasattr(components, '__iter__'):
            raise TypeError("components must be a collection")
        if not is_numeric(components):
            raise TypeError("components must be numeric values")
        if len(components) == 0:
            raise ValueError("vectors cannot be empty")
        self._components = list(components)

    def __str__(self):
        return "<" + ", ".join([str(i) for i in self._components]) + ">"

    def __repr__(self):
        return "geom.Vector("+str(self._components)+")"

    def __len__(self):
        return len(self._components)

    def __getitem__(self, i):
        if i >= len(self):
            raise IndexError("Vector has less than %d dimensions" % (i+1))
        return self._components[i]

    def __iter__(self):
        yield from self._components

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
            raise TypeError("Added vector must have numeric components")
        if len(other) != len(self):
            raise ValueError("Cannot add vectors of two different dimensions")
        return Vector([a + b for a, b in zip(self, other)])

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not is_numeric(other):
            raise TypeError("Subtracted vector must have numeric components")
        if len(other) != len(self):
            raise ValueError("Cannot subtract vectors of two different " +
                             "dimensions")
        return Vector([a - b for a, b in zip(self, other)])

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not is_numeric(other):
            raise TypeError("Second argument must be numeric")
        if isinstance(other, numbers.Number):
            return Vector([other*c for c in self])
        if len(self) != 3 or len(other) != 3:
            raise ValueError("Can only perform cross products in R3")
        cross = Vector([self[1]*other[2] - self[2]*other[1],
                        self[2]*other[0] - self[0]*other[2],
                        self[0]*other[1] - self[1]*other[0]])
        return cross

    def __rmul__(self, other):
        if not is_numeric(other):
            raise TypeError("Second argument must be numeric")
        if isinstance(other, numbers.Number):
            return self * other
        if len(self) != 3 or len(other) != 3:
            raise ValueError("Can only perform cross products in R3")
        cross = Vector([other[1]*self[2] - other[2]*self[1],
                        other[2]*self[0] - other[0]*self[2],
                        other[0]*self[1] - other[1]*self[0]])
        return cross

    def __truediv__(self, m):
        if not isinstance(m, numbers.Number) or isinstance(m, bool):
            raise TypeError("Vectors can only be divided by a scalar")
        return Vector([i/m for i in self])

    def __matmul__(self, other):
        if not is_numeric(other):
            raise TypeError("Can only perform dot produt on numeric vectors")
        if len(self) != len(other):
            raise ValueError("Cannot perform dot product on vectors of two " +
                             "different dimensions")
        return sum([a*b for a, b in zip(self, other)])

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

    def mag(self):
        """Compute the magnitude of this vector. Equivalent to `abs(v)`."""
        return abs(self)

    def magSq(self):
        """Compute the square of the magnitude of this vector."""
        return sum([a*a for a in self])

    def add(self, other):
        """Return the sum of this vector and the vector `other`.
        
        Equivalent to `v + other`. TypeError is raised if `other` is not a
        numeric collection the same length as this vector.
        """
        return self + other

    def addOn(self, other):
        """Add `other` to this vector.

        Similar to `v.add(other)` or `v + other`, but `v.addOn(other)` mutates
        this `v`. TypeError is raised if `other` is not a numeric collection.
        ValueError is raised if the vectors are not the same length.
        """
        if not is_numeric(other):
            raise TypeError("Added vector must be numeric")
        if len(other) != len(self):
            raise ValueError("Added vector must have same dimensions")
        for i in range(len(self)):
            self[i] += other[i]

    def sub(self, other):
        """Return the difference of this vector and the vector `other`.

        Equivalent to `v - other`. TypeError is raised if `other` is not a
        numeric collection the same length as this vector.
        """
        return self - other

    def takeAway(self, other):
        """Subtract the vector `other` from this vector.

        Similar to `v.sub(other)` or `v - other`, but `v.takeAway(other)`
        mutates this vector. TypeError is raised if `other` is not a numeric
        collection the same length as this vector.
        """
        if not is_numeric(other):
            raise TypeError("Added vector must be numeric")
        if len(other) != len(self):
            raise ValueError("Added vector must have same dimensions")
        for i in range(len(self)):
            self[i] -= other[i]

    def mul(self, m):
        """Return the product of this vector and the scalar `m`.

        Equivalent to `v * m`. TypeError is raised if m is not a number.
        """
        if not isinstance(m, numbers.Number) or isinstance(m, bool):
            raise TypeError("Vectors can only be multiplied by scalars")
        return Vector([i*m for i in self])

    def mulBy(self, m):
        """Multiply this vector by the scalar `m`.

        Similar to `v * m` or `v.mul(m)`, but `v.mulBy(m)` mutates the vector
        `v`. TypeError is raised if m isn't a number.
        """
        if not isinstance(m, numbers.Number) or isinstance(m, bool):
            raise TypeError("Vectors can only be multiplied by scalars")
        for i in range(len(self)):
            self[i] *= m

    def div(self, m):
        """Return the quotient of this vector the scalar `m`.
        
        Equivalent to `v / m`. TypeError is raised if m isn't a number.
        """
        return self/m

    def divBy(self, m):
        """Divide this vector by the scalar `m`.

        Similar to `v / m` or `v.div(m)`, but `v.divBy(m)` mutates this the
        vector `v`. TypeError is raised if m isn't a number.
        """
        if not isinstance(m, numbers.Number) or isinstance(m, bool):
            raise TypeError("Vectors can only be divided by scalars")
        for i in range(len(self)):
            self[i] /= m

    def normalize(self):
        """Normalize this vector.

        Similar to `v.norm()` or `~v`, but `v.normalize()` mutates `v` instead
        of returning a new vector. ValueError is raised if this vector is
        the zero vector.
        """
        if abs(self) == 0:
            raise ValueError("Cannot normalize the zero vector")
        self.divBy(abs(self))

    def dot(self, other):
        """Return the dot product of this vector and `other`.
        
        Equivalent to `v @ other`. TypeError is raised if `other` is not a
        numeric collection. ValueError is raised if this vector and `other` are
        not of the same dimension.
        """
        return self @ other

    def cross(self, other):
        """Return the cross product of this vector and `other`.

        Equivalent to `v * other`. TypeError is raised if `other` is not a
        numeric collection. ValueError is raised if this vector and `other` are
        not in R3.
        """
        return self * other

    def norm(self):
        """Return a normalized version of this vector. Equivalent to `~v.`"""
        return ~self

class Circle(object):
    """A Circle stores basic circle info and provides relevant useful methods.
    """
    __slots__ = ['_center', '_radius']
    def __init__(self, center, radius):
        """Create a circle with a given ``center`` and ``radius``.

        TypeError is raised if center is not a numeric collection or if radius
        is not a number. ValueError is raised if center is not in R2 or if
        radius is not a real non-negative number.
        """
        self.center = center
        self.radius = radius

    @property
    def center(self):
        """The center of the circle.

        center is stored as a Vector. Setting center will raise TypeError if
        it's not numeric, AttributeError if has no length, and ValueError
        if it's not in R2.
        """
        return self._center
    @center.setter
    def center(self, center):
        if not is_numeric(center):
            raise TypeError("center must be numeric")
        if not hasattr(center, '__len__'):
            raise AttributeError("center must have a length attribute")
        if len(center) != 2:
            raise ValueError("center must be in R2")
        self._center = Vector(center)

    @property
    def radius(self):
        """The radius of the circle.

        Setting radius will raise TypeError if it's not numeric and ValueError
        if it's negative.
        """
        return self._radius
    @radius.setter
    def radius(self, r):
        if not is_numeric(r):
            raise TypeError("radius must be numeric")
        if r < 0:
            raise ValueError("radius must be non-negative")
        self._radius = r
