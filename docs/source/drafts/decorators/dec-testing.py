#! /usr/bin/env python

def foo_dec(f):
    # just grab it all
    def wrapper(*args, **kwargs):
        print 'Inside dec: {0}, {1}'.format(args, kwargs)
        return f(*args, **kwargs)
    return wrapper

def bar(z, c):
    print "Inside func: {0}, {1}".format(z, c)
bar = foo_dec(bar)

bar(c=4, z=2)
