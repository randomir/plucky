plucky: concise deep obj.get()
==============================

.. image:: https://img.shields.io/pypi/v/plucky.svg
    :target: https://pypi.python.org/pypi/plucky

.. image:: https://img.shields.io/pypi/l/plucky.svg
    :target: https://pypi.python.org/pypi/plucky

.. image:: https://img.shields.io/pypi/wheel/plucky.svg
    :target: https://pypi.python.org/pypi/plucky

.. image:: https://img.shields.io/pypi/pyversions/plucky.svg
    :target: https://pypi.python.org/pypi/plucky

.. image:: https://api.travis-ci.org/randomir/plucky.svg?branch=master
    :target: https://travis-ci.org/randomir/plucky


``plucky.pluckable`` happily wraps dictionary- or list-like objects and allows
for chained soft plucking with attribute and item getters (e.g. ``.attr``,
``["key"]``, ``[idx]``, ``[a:b]``, or a combination: ``["key1", "key2"]``,
and ``[0, 3:7, ::-1]``; even: ``["length", 0:5]``).

``plucky.pluck`` will allow you to pluck *just as with* ``pluckable`` (plucking
syntax is the same), but accepting a string selector instead of a Python
expression.

``plucky.plucks`` enables you to safely extract several-levels deep values by
using a concise string selector comprised of dictionary-like keys and list-like
indices. Stands for *pluck simplified*, since it supports only a subset of
``pluck`` syntax. It's simpler and a bit faster.

``plucky.merge`` facilitates recursive merging of two data structures, reducing
leaf values with the provided binary operator.


Installation
------------

``plucky`` is available as a **zero-dependency** Python package. Install with::

    $ pip install plucky


Usage
-----

.. code-block:: python

    from plucky import pluck, plucks, pluckable, merge

    pluckable(obj).users[2:5, 10:15].name["first", "middle"].value

    pluck(obj, 'users[2:5, 10:15].name["first", "middle"]')

    plucks(obj, 'users.2:5.name.first')

    merge({"x": 1, "y": 0}, {"x": 2})


Examples
--------

.. code-block:: python

    obj = {
        'users': [{
            'uid': 1234,
            'name': {
                'first': 'John',
                'last': 'Smith',
            }
        }, {
            'uid': 2345,
            'name': {
                'last': 'Bono'
            }
        }, {
            'uid': 3456
        }]
    }

    plucks(obj, 'users.1.name')
    # -> {'last': 'Bono'}

    plucks(obj, 'users.name.last')
    # -> ['Smith', 'Bono']

    plucks(obj, 'users.*.name.first')
    # -> ['John']

    pluckable(obj).users.name.first.value
    # -> ['John']

    pluckable(obj).users.uid[0, 2, 1].value
    # -> [1234, 3456, 2345]

    pluckable(obj, skipmissing=False, default='Unnamed').users.name.first.value
    # -> ['John', 'Unnamed', 'Unnamed']


More Examples! :)
-----------------

.. code-block:: python

    pluckable(obj).users[:, ::-1].name.last.value
    # -> ['Smith', 'Bono', 'Bono', 'Smith']

    pluckable(obj).users[:, ::-1].name.last[0, -1].value
    # -> ['Smith', 'Smith']

    pluck(obj, 'users[:, ::-1].name.last[0, -1]')
    # -> ['Smith', 'Smith']

    plucks([1,2,3], '-2:')
    # -> [2,3]

    plucks([1,2,3], '::-1')
    # -> [3,2,1]

    plucks([1, {'val': 2}, 3], 'val')
    # -> [2]

    plucks([1, {'val': [1,2,3]}, 3], '1.val.-1')
    # -> 3

    merge({"x": 1, "y": 0}, {"x": 2})
    # -> {"x": 3, "y": 0}

    merge({"a": [1, 2], "b": [1, 2]}, {"a": [3, 4], "b": [3]})
    # -> {"a": [4, 6], "b": [1, 2, 3]}
