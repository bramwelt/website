Decorators
==========

Python decorators are really just syntactic sugar for a function wrapper.

::

    @bar
    def foo(...):
        ...
        
Here bar is the *decorator* and foo is the function
bar *decorates*. This example could have also been written::

    def foo(...):
        ...

    foo = bar(foo)

These decorators allow you - developers - to do things before and/or
after a function is called. That has great implications for easily
implementing things like `memoization`_, `deprecation warnings`_, or
`authorization`_.

Decorators are absolutely daugnting at first glance though. Any
programmer would run away screaming they moment they saw a function
nested 3 times.[1] It took a week of staring at the code, and reading
everything I could find on decorators before they finally clicked.

- - -

Though decorators are an advanced Python construct, they are really a simple
concept wrapped in some syntactic sugar.

In Python a decorator is used by adding a function call, prefixed with
'@' just before a function or method definition.

Decorators in Python `originally`_ started as a way to easily apply
`staticmethod` and `classmethod`  to Python objects, and they are aptly
named because they are used to *decorate* the methods of a class.

.. A `staticmethod` is a method accessable from a class without requiring
   an instance of that class. 

.. A `classmethod` is a method that is the same across all classes, similar
   to 'static' in Java


.. _originally: http://www.python.org/dev/peps/pep-0318/
.. _memoization: http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
.. _singletons: http://wiki.python.org/moin/PythonDecoratorLibrary#The_Sublime_Singleton
.. _deprecation warnings: http://wiki.python.org/moin/PythonDecoratorLibrary#Smart_deprecation_warnings_.28with_valid_filenames.2C_line_numbers.2C_etc..29
.. _authorization: https://wiki.python.org/moin/PythonDecoratorLibrary#Access_control

I will be showing you how decorators were originally used, how they are
used with functions without any arguments, functions with arguments,
and class methods. After that we will look at class based decorators and
finish on a meta note with a decorator for your decorators.

Without Syntax
--------------

At first glace decorators may seem like a bit of magic, but they are
really just syntactic sugar.

This is how decorators were originally used, and is shown first as it
may help understand how the functions are arranged later on when the
actual syntax is used.

Without Arguments
~~~~~~~~~~~~~~~~~

::

    def spam(f):
        """
        Spam before function.
        """
        def print_spam():
            f()
            print "spam, spam, spam!"
        return print_spam

    def my_func():
        print "I like..."

    my_func = print_spam(my_func)


What is really happening is that the function `my_func` is being rebound
to the return value of `spam`. As you can see from the example, `spam`
is passed `my_func` as an argument and constructs a new function
`print_spam` that calls the first function before printing 'spam' three times.

With Arguments
~~~~~~~~~~~~~~



Python Syntax
-------------

Without Arguments
~~~~~~~~~~~~~~~~~

>>> def my_dec(f):
...     def print_hello():
...         print 'Hello, ',
...         f()
...     return print_hello
... 
>>> @my_dec
... def print_world():
...     print 'world!'
... 
>>> print_world
<function print_hello at 0x7f3cf55456e0>
>>> print_world()
Hello, world!
>>>

.. Note: Decorators that do not take arguments are written without
         parentheticals. '@my_dec()' will raise a 'TypeError'

With Arguments
~~~~~~~~~~~~~~

>>> def append_str(msg):
...     def wrap(f):
...         def special_msg():
...             return "{}{}".format(msg, f())
...         return special_msg
...     return wrap
...
>>> @append_str("Some call me...")
... def my_name():
...     return 'Tim'
...
>>> print my_name()


Class Based Decorators
----------------------

Without Arguments
~~~~~~~~~~~~~~~~~

With Arguments
~~~~~~~~~~~~~~

Functool Wraps
--------------

Decorators for Classes and Functions
------------------------------------

::

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
            print "Args: {0}\nKwargs: {1}".format(str(args), str(kwargs))
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
        print(output.format(multiply(3, 4), multiply))

        f = Foo()
        print(output.format(f.multiply(3, 4), f.multiply))



.. _12-steps: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/ 



[1] The first time I came across them I was doing Twisted
development, and they also included Deferreds. Which, if you know
anything about Twisted, is an entirely seperate beast.
