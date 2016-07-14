def pluck(obj, selector, default=None):
    """Safe itemgetter for structured objects."""
    
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
