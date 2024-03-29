.. geom documentation master file, created by
   sphinx-quickstart on Sun Apr 21 09:11:02 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

geom Documentation
==================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

About
-----
geom (pronounced "jom") is a a module for working with geometry in a pythonic
way. The motivation behind it's development was to use as a base for collision
detection, but the functionality offered by the module offers much more depth.

Reference
---------
.. automodule:: geom

Functions
---------
.. autofunction:: is_numeric

Classes
-------

Vector
------
.. autoclass:: Vector

Vector Methods
^^^^^^^^^^^^^^
.. automethod:: Vector.__init__
.. automethod:: Vector.mag
.. automethod:: Vector.magSq
.. automethod:: Vector.norm
.. automethod:: Vector.normalize
.. automethod:: Vector.add
.. automethod:: Vector.addOn
.. automethod:: Vector.sub
.. automethod:: Vector.takeAway
.. automethod:: Vector.mul
.. automethod:: Vector.mulBy
.. automethod:: Vector.div
.. automethod:: Vector.divBy
.. automethod:: Vector.dot
.. automethod:: Vector.cross

Circle
------
.. autoclass:: Circle
.. autoattribute:: Circle.center
.. autoattribute:: Circle.radius
.. autoattribute:: Circle.area
.. autoattribute:: Circle.circumference

Circle Methods
^^^^^^^^^^^^^^
.. automethod:: Circle.__init__
.. automethod:: Circle.scaled_to
.. automethod:: Circle.scaled_by
.. automethod:: Circle.moved_to
.. automethod:: Circle.moved_by
.. automethod:: Circle.intersects

.. Indices and tables
.. ==================
.. 
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
