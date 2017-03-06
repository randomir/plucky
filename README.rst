plucky: concise deep obj.get()
==============================

``plucky.pluck`` enables you to safely extract several-levels deep values by 
using a concise selector comprised of dictionary-like keys and list-like 
indices. Slices over list items are also supported.

``plucky.merge`` facilitates recursive merging of two data structures, reducing
leaf values with the provided binary operator.


Installation
------------

``plucky`` is available as a **zero-dependency** Python package. Install with::

    $ pip install plucky


Usage
-----

.. code-block:: python

    from plucky import pluck, merge

    pluck(obj, 'selector.*.path.2')

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
        }]
    }

    pluck(obj, 'users.1.name')
    # -> {'last': 'Bono'}

    pluck(obj, 'users.*.name.last')
    # -> ['Smith', 'Bono']

    pluck(obj, 'users.*.name.first')
    # -> ['John']


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
