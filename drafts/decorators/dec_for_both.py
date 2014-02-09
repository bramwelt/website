from functools import wraps

# Decorator that works on both functions and methods
def func_or_method(f):
    """
    This decorator prints "hello world" and works on both functions and
    methods.
    """
    def call(f, self, *args, **kwargs):
        if self is None:
            return f(*args, **kwargs)
        return f(self, *args, **kwargs)

    @wraps(f)
    def wrapper(*args, **kwargs):
        print "hello, world"
        return call(f, *args, **kwargs)
    return wrapper

# Dummy Function
@func_or_method
def multiply(a, b):
    """
    Just a basic function.
    """
    return a*b

# Dummy Class
class Foo(object):
    """
    Just a basic class.
    """

    @func_or_method
    def multiply(self, a, b):
        """
        Just a basic method.
        """
        return a*b
        
if __name__ == "__main__":
    output = "Output: {}\nReference: {}\n"
    print(output.format(multiply(2, 8), multiply))

    f = Foo()
    print(output.format(f.multiply(3, 4), f.multiply))
