import geom
import pytest
import math
import sys

def test_one_dimension():
    """Test equality for vectors with one dimension"""
    assert geom.Vector([1]) == geom.Vector([1])

def test_many_dimensions():
    """Test equality for vectors with multiple dimensions"""
    assert geom.Vector([1, 2, 3]) == geom.Vector([1, 2, 3])

def test_zero_equality():
    """Test that zero vectors are equal"""
    assert geom.Vector([0, 0]) == geom.Vector([0, 0])

def test_negative_equality():
    """Test that vectors with negative components are equal"""
    assert geom.Vector([-1, 2]) == geom.Vector([-1, 2])

def test_reflexive():
    """Test that vector equality is reflexive"""
    a = geom.Vector([13, -54, 12])
    assert a == a

def test_symmetric():
    """Test that vector equality is symmetric"""
    a = geom.Vector([-3, -1])
    b = geom.Vector([-3, -1])
    assert a == b
    assert b == a

def test_transitive():
    """Test that vector equality is transitive"""
    a = geom.Vector([1, 1, 1, 1])
    b = geom.Vector([1, 1, 1, 1])
    c = geom.Vector([1, 1, 1, 1])
    assert a == b
    assert b == c
    assert a == c

def test_null_equality():
    """Test that null equality is false"""
    assert not geom.Vector([0]) == None

def test_with_floats():
    """Test that equality works with floating point numbers."""
    assert geom.Vector([1.2, 1.3]) == geom.Vector([1.2, 1.3])

def test_with_small_floats():
    """Test that equality works with small floating point numbers."""
    a = geom.Vector([0.0001, 0.0002, -0.0003])
    b = geom.Vector([0.0001, 0.0002, -0.0003])
    assert a == b

def test_with_large_floats():
    """Test that equality works with large floating point numbers."""
    a = geom.Vector([123456.7, 891011.12])
    b = geom.Vector([123456.7, 891011.12])
    assert a == b

def test_with_complex_numbers():
    """Test that equality works with complex numbers."""
    a = geom.Vector([complex(1, 1), complex(-1, -1)])
    b = geom.Vector([complex(1, 1), complex(-1, -1)])
    assert a == b

def test_with_multiple_types():
    """Test that equality works with multiple types."""
    a = geom.Vector([1.0, -3, complex(0, 0.2)])
    b = geom.Vector([1.0, -3, complex(0, 0.2)])
    assert a == b

def test_same_value_different_types():
    """Test that equality works with same value but different types."""
    assert geom.Vector([3.0]) == geom.Vector([complex(3.0)])

def test_with_max_float():
    """Test that equality works with max float values"""
    a = geom.Vector([sys.float_info.max, -sys.float_info.max])
    b = geom.Vector([sys.float_info.max, -sys.float_info.max])
    assert a == b

def test_with_infinity():
    """Test that equality works with infinity in components"""
    a = geom.Vector([-0.3, math.inf, -math.inf])
    b = geom.Vector([-0.3, math.inf, -math.inf])
    assert a == b

def tests_with_infinity_different_components():
    """Test that equality doesn't work when infinity components aren't the same"""
    a = geom.Vector([1, -math.inf, 2])
    b = geom.Vector([-math.inf, 1, 2])
    assert not a == b

def test_with_NaN():
    """Test that equality doesn't work with NaN components"""
    a = geom.Vector([1, float('nan'), 3])
    b = geom.Vector([1, float('nan'), 3])
    assert not a == b
