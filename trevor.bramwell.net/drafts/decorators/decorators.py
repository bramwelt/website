# Without Arguments
def my_dec(f):
    def print_hello():
        print 'Hello, ',
        return f()
    return print_hello

# With Arguments
def append_str(msg):
    def wrap(f):
        def special_msg():
            return "{}{}".format(msg, f())
        return special_msg
    return wrap


def some_call_me(func):
    def wrap():
        print 'Some call me...',
        return func()
    return wrap


def tim():
    print 'Tim'

tim = some_call_me(tim)

if __name__ == '__main__':
    tim()
    # Without Arguments
    #@my_dec
    #def print_world():
    #    print 'world!'
    
    #print print_world
    #print_world()

    # Without Arguments (TypeError)
    #@my_dec()
    #def print_world2():
    #    print 'world!'
    #
    #print print_world2
    #print_world2()

    # With Arguments
    @append_str("Some call me...")
    def my_name():
        return 'Tim'

    print my_name()
