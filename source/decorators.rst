Decorators
==========

Decorators in Python `originally`_ started as a way to easily convert
methods on Python objects to static and class methods. They are aptly
named because they are used to *decorate* methods of a class.

.. _originally: http://www.python.org/dev/peps/pep-0318/

Decorators are really a simple concept wrapped in some syntactic sugar
which can greatly reduce a lot of redundant code (keep things `DRY`_),
and enable some design patterns like `memoization`_, `deprecation
warnings`_, or `authorization`_ to be applied easily to any method.

.. _DRY: http://en.wikipedia.org/wiki/Don%27t_repeat_yourself

At first glance, decorators were absolutely daughting to me. I was
introduced to a `Twisted`_ code base with some decorators that contained
more than 3 nested functions, along with `Deferreds`_.

.. _memoization: http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
.. _deprecation warnings: http://wiki.python.org/moin/PythonDecoratorLibrary#Smart_deprecation_warnings_.28with_valid_filenames.2C_line_numbers.2C_etc..29
.. _authorization: https://wiki.python.org/moin/PythonDecoratorLibrary#Access_control
.. _Twisted: http://twistedmatrix.com
.. _Deferreds: http://twisted.readthedocs.org/en/latest/core/howto/defer.html


Overview
--------

I will be showing you how decorators were originally used. This will be
followed by an examination of decorators on functions with arguments,
without arguments, on methods with arguments, and without arguments.
Finally that we will look at class based decorators and finish with a
somewhat meta examination of decorators for decorators.

Without Syntax
--------------

This first example shows how decorators were originally used::

    def foo(...):
        ...

    foo = bar(foo)

In this example a function `foo` is defined, and the subsequently
reassigned as the function `bar` which takes `foo` as it's argument.
`bar` here is actually the decorator, and will later call `foo` thus
allowing `bar` to do work during, or after `foo` executes.

Syntax
------

In Python a decorator is applied by prefixing a function with '@' (such
as `@bar`), and writing that just before another function definition.

For example::

    @bar
    def foo(...):
        ...
        
Here bar is *decorating* foo. 

Without Arguments
~~~~~~~~~~~~~~~~~

A trivial example is a decorator that prints: `spam, spam spam!` after
each time a function is called::

    def spam(f):
        """
        Spam before function.
        """
        def print_spam():
            f()
            print "spam, spam, spam!"
        return print_spam

    @spam
    def my_func():
        print "I like..."

It is important to note here that decorators return functions. Let me
say that again, in bigger letters.

.. attention:: DECORATORS RETURN FUNCTIONS

So `my_func` gets called, which has actually been redefined to `my_func
= span(my_func)`. So its actually `spam` which gets called, with
`my_func` as it's only argument (here redefined to `f` within `my_func`).

So `spam` starts executing ... which returns a function it has defined
called `print_spam`. (Are you starting to see why this is confusing?
Stop it! They're smarter than that!).

So `print_spam` gets executed, which, because it was defined within the
scope of `spam`, has a reference to `f`, which is really `my_func`.

So `my_func` _finally_ gets called, `spam, spam, spam!` is printed, and
the function exits.

Phew!


With Arguments
~~~~~~~~~~~~~~

Now, lets try this again. What we'd really like is the ability to print
*any* string after the function executes. So instead of having `spam,
spam, spam!` as part of the decorator, we'll pass it in as an argument!

::

    def spam(f, a_silly_string):
        """
        Spam before function.
        """
        def print_spam():
            f()
            print a_silly_string
        return print_spam

    @spam("spam, spam, spam!")
    def my_func():
        print "I like..."

The only difference here from the previous example, is that `spam` now
takes an argument: `a_silly_string`. This argument is printed within
`print_spam` and passed as the only argument to the `@spam` decorator.

See! You're starting to get the hang of this!

Class Based Decorators
----------------------

Now for something complete different!

(... well, not really, but who *doesn't* like Monty Python?)

Without Arguments
~~~~~~~~~~~~~~~~~

::

    def spam(f):
        """
        Print spam
        """

        def print_spam(self):
             f(self)
             print "spam, spam, spam!"

        return print_spam

    class Foo(object):
        """
        Foo prints a message
        """

        @spam
        def bar(self):
            print "I like..."


With Arguments
~~~~~~~~~~~~~~

::

    def spam(f):
        """
        Print spam
        """

        def print_spam(self, a_silly_string):
             f(self)
             print a_silly_string

        return print_spam

    class Foo(object):
        """
        Foo prints what it likes
        """

        @spam("eggs, eggs, and spam")
        def bar(self):
            print "I like..."



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
