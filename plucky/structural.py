"""
pluckable - a dict/list lazy wrapper that supports chained soft get/slice,
like::

    pluckable(obj).users[2:5, 10:15].name.first

    pluckable(obj)[::-1].meta["is-admin"][0]

"""


class pluckable(object):
    def __init__(self, obj, default=None):
        self.obj = obj
        self.default = default
    
    @property
    def value(self):
        return self.obj
    
    def _filtered_list(self, selector):
        """Iterate over `self.obj` list, extracting `selector` from each
        element. The `selector` can be a simple integer index, slice object,
        or any valid dict key (hashable object).
        """
        res = []
        for elem in self.obj:
            try:
                res.append(elem[selector])
            except:
                pass
        return res
    
    def _get(self, name):
        if isinstance(self.obj, list):
            obj = self._filtered_list(name)
        else:
            try:
                obj = self.obj[name]
            except:
                obj = self.default
        return pluckable(obj, self.default)
    
    def __getattr__(self, name):
        """Handle ``obj.name`` lookups.
        
            obj.key -> the same as obj["key"]: if obj is a dict, extract value
                       under key "key" (or default val), if obj is a list,
                       iterate over all elements, extracting "key" from each
                       element
        """
        return self._get(name)
    
    def __str__(self):
        return str(self.obj)

    def __repr__(self):
        return repr(self.obj)
