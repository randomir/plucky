plucky: concise deep obj.get()
==============================

``plucky.pluck`` enables you to safely extract several-levels deep values by 
using a concise selector comprised of dictionary-like keys and list-like 
indices. Wildcards over list items are also supported.


Installation
------------

``plucky`` is available as a Python package. Install with::

    $ pip install plucky


Usage
-----

.. code-block:: python

    from plucky import pluck

    pluck(obj, 'selector.*.path.2')


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

    pluck([1, {'val': 2}, 3], '*.val')
    # -> [2]

    pluck([1, {'val': [1,2,3]}, 3], '1.val.-1')
    # -> 3

