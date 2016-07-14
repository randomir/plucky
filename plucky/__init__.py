"""
Plucking (deep) keys/paths safely from python collections has never been easier.
"""

__title__ = 'plucky'
__version__ = '0.1'
__author__ = 'Radomir Stevanovic'
__author_email__ = 'radomir.stevanovic@gmail.com'
__copyright__ = 'Copyright 2014 Radomir Stevanovic'
__license__ = 'MIT'
__url__ = 'https://github.com/randomir/plucky'



def pluck(obj, selector, default=None):
    """Safe itemgetter for structured objects.
    Happily operates on all (nested) objects that implement the item getter, 
    i.e. the `[]` operator.

    The `selector` is ~ ``(<key>|<index>|\*)(\.(<key>|<index>|\*))*``.
    Parts (keys) in the selector path are separated with a dot. If the key
    looks like a number it's interpreted as such, i.e. as an index (so beware
    of numeric string keys in `dict`s).
    A special key is `*`, representing the slice-all op `[:]`.

    Examples:
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
            -> {'last': 'Bono'}

        pluck(obj, 'users.*.name.last')
            -> ['Smith', 'Bono']

        pluck(obj, 'users.*.name.first')
            -> ['John']


    Note: since the dot `.` is used as a separator, keys can not contain dots.

    TODO: Indexing with [], slices, escaped keys.
    """
    
    def _filter(iterable, index):
        res = []
        for obj in iterable:
            try:
                res.append(obj[index])
            except:
                pass
        return res
    
    miss = False
    for key in selector.split('.'):
        try:
            index = int(key)
        except:
            if key == '*':
                index = slice(None)
            else:
                index = key
        
        if miss:
            if isinstance(index, basestring):
                obj = {}
            else:
                obj = []
        
        try:
            if isinstance(index, basestring):
                if isinstance(obj, list):
                    obj = _filter(obj, index)
                else:
                    obj = obj[index]
            else:
                obj = obj[index]
            miss = False
        except:
            miss = True
    
    if miss:
        return default
    else:
        return obj
