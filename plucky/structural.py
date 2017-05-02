"""
pluckable - a dict/list lazy wrapper that supports chained soft get/slice,
like::

    pluckable(obj).users[2:5, 10:15].name.first

    pluckable(obj)[::-1].meta["is-admin"][0]

"""
from __future__ import absolute_import

import sys

from .compat import xrange, baseinteger


class pluckable(object):
    def __init__(self, obj=None, default=None, skipmissing=True, _empty=False):
        """Creates a new pluckable object based on `obj`. Default value for the
        missing keys is given with `default`.

        A two modes of plucking are supported::

        (1) the default, document databases alike, where missing keys (and it's
            ancestors) will be silently dropped-out -- except for the leaf
            nodes -- which always default to the ``default`` when missing.

        (2) one-on-one extractor (explict mode), which will include all missing
        values as ``default``, ensuring the leaf values exist even when one (or
        more) intermediate nodes are missing.
        """
        self.obj = obj
        self.default = default
        self.skipmissing = skipmissing
        self._empty = _empty
    
    @property
    def value(self):
        if self._empty:
            return self.default
        else:
            return self.obj
    
    def _filtered_list(self, selector):
        """Iterate over `self.obj` list, extracting `selector` from each
        element. The `selector` can be a simple integer index, or any valid dict
        key (hashable object).
        """
        res = []
        for elem in self.obj:
            try:
                res.append(elem[selector])
            except:
                if not self.skipmissing:
                    res.append(self.default)
        return res

    def _sliced_list(self, selector):
        """For slice selectors operating on lists, we need to handle them
        differently, depending on ``skipmissing``. In explicit mode, we may have
        to expand the list with ``default`` values.
        """
        if self.skipmissing:
            return self.obj[selector]

        # TODO: can be optimized by observing list bounds
        keys = xrange(selector.start or 0,
                      selector.stop or sys.maxint,
                      selector.step or 1)
        res = []
        for key in keys:
            try:
                res.append(self.obj[key])
            except:
                res.append(self.default)
        return res

    def _extract_from_list(self, selector):
        if isinstance(selector, baseinteger):
            return self._sliced_list(slice(selector, selector+1))
        elif isinstance(selector, slice):
            return self._sliced_list(selector)
        else:
            return self._filtered_list(selector)
    
    def _extract_from_dict(self, selector):
        """Extracts all values from `self.obj` dict addressed with a `selector`.
        Selector can be a ``slice``, or a singular value extractor in form of a
        valid dictionary key (hashable object).
        
        If `selector` is a singular value extractor (like a string, integer,
        etc), a single value (for a given key) is returned if key exists, an
        empty list if not.
        
        If `selector` is a ``slice``, each key from that range is extracted;
        failing-back, again, to an empty list.
        """
        if isinstance(selector, slice):
            keys = xrange(selector.start or 0,
                          selector.stop or sys.maxint,
                          selector.step or 1)
        else:
            keys = [selector]
        
        res = []
        for key in keys:
            try:
                res.append(self.obj[key])
            except:
                if not self.skipmissing:
                    res.append(self.default)
        return res
    
    def _get_all(self, *selectors):
        res = []
        for selector in selectors:
            if isinstance(self.obj, list):
                res.extend(self._extract_from_list(selector))
            else:
                res.extend(self._extract_from_dict(selector))
        
        singular_selector = \
            not isinstance(self.obj, list) or \
            len(selectors) == 1 and isinstance(selectors[0], baseinteger)
        
        if len(res) == 0:
            return pluckable(_empty=True, default=self.default,
                             skipmissing=self.skipmissing)
        elif len(res) == 1 and singular_selector:
            return pluckable(res[0], self.default,
                             skipmissing=self.skipmissing)
        else:
            return pluckable(res, self.default,
                             skipmissing=self.skipmissing)
    
    def __getattr__(self, name):
        """Handle ``obj.name`` lookups.
        
            obj.key -> the same as obj["key"]: if obj is a dict, extract value
                       under key "key" (or default val), if obj is a list,
                       iterate over all elements, extracting "key" from each
                       element
        """
        return self._get_all(name)
    
    def __getitem__(self, key):
        """Handle various ``obj[key]`` lookups, including::
        
            obj[2]      -> if obj is list, extract elem with index 2;
                           if obj is dict, extract value under key 2
            obj[1, 2]   -> if obj is list, extract elems with indices 1 and 2;
                           if obj is dict, extract values under keys 1,2 into a new list
            obj[1:5]    -> the same as obj[1,2,3,4,5]
            obj["key"]  -> if obj is dict, extract value under key "key" (or default val),
                           if obj is list, iterate over all elements, extracting "key" from each element
            obj[2, 4:5] -> the same as obj[2,4,5]
            obj[1:, 0]  -> analog to the above, sugar syntax for: obj[1:] + [obj[0]]
            obj["x", "y"]  -> if obj is dict, extract keys "x" and "y" into a new list;
                              if obj is list, iterate over all elements, extracting "x" and "y"
                              from each element into a flat list
            obj["x", "y", 3, ::-1] -> similar to above, extracting "x", "y", 3 and all keys in reverse
        """
        if isinstance(key, tuple):
            return self._get_all(*key)
        else:
            return self._get_all(key)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)
