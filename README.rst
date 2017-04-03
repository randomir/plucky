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


``plucky.pluck`` enables you to safely extract several-levels deep values by 
using a concise selector comprised of dictionary-like keys and list-like 
indices. Slices over list items are also supported.

``plucky.pluckable`` will happily wrap dictionary- or list-like objects and allow
for chained soft plucking with attribute and item getters (e.g. ``.attr``,
``["key"]``, ``[idx]``, ``[a:b]``, or a combination: ``["key1", "key2"]``,
and ``[0, 3:7, ::-1]``)

``plucky.merge`` facilitates recursive merging of two data structures, reducing
leaf values with the provided binary operator.


Installation
------------

``plucky`` is available as a **zero-dependency** Python package. Install with::

    $ pip install plucky


Usage
-----

.. code-block:: python

    from plucky import pluck, merge, pluckable

    pluck(obj, 'selector.*.path.2')

    merge({"x": 1, "y": 0}, {"x": 2})
    
    pluckable(obj).users[2:5, 10:15].name["first", "middle"]


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

    pluck(obj, 'users.1.name')
    # -> {'last': 'Bono'}

    pluck(obj, 'users.*.name.last')
    # -> ['Smith', 'Bono']

    pluck(obj, 'users.*.name.first')
    # -> ['John']

    pluckable(obj).users.name.first.value
    # -> ['John']

    pluckable(obj).users.uid.value[0, 2, 1]
    # -> [1234, 3456, 2345]

    pluckable(obj, skipmissing=False, default='Unnamed').users.name.first.value
    # -> ['John', 'Unnamed', 'Unnamed']


More Examples! :)
-----------------

.. code-block:: python

    pluck([1,2,3], '2')
    # -> 3

    pluck([1,2,3], '-1')
    # -> 3

    pluck([1,2,3], '*')
    # -> [1,2,3]

    pluck([1,2,3], '-2:')
    # -> [2,3]

    pluck([1,2,3], '::-1')
    # -> [3,2,1]

    pluck([1, {'val': 2}, 3], '*.val')
    # -> [2]

    pluck([1, {'val': [1,2,3]}, 3], '1.val.-1')
    # -> 3

    merge({"x": 1, "y": 0}, {"x": 2})
    # -> {"x": 3, "y": 0}

    merge({"a": [1, 2], "b": [1, 2]}, {"a": [3, 4], "b": [3]})
    # -> {"a": [4, 6], "b": [1, 2, 3]}

    pluckable(obj).users.name.last.value
    # -> ['Smith', 'Bono']

    pluckable(obj).users[:, ::-1].name.last.value
    # -> ['Smith', 'Bono', 'Bono', 'Smith']
    
    pluckable(obj).users[:, ::-1].name.last[0, -1].value
    # -> ['Smith', 'Smith']
