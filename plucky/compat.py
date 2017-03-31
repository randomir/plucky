"""Simple python 2/3 compatibility fixes to avoid dependance on the `six`
package."""


# for simpler string detection
try:
    basestring = basestring
except:
    basestring = str

# xrange for python3
try:
    xrange = xrange
except:
    xrange = range
