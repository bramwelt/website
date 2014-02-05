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

my_func = spam(my_func)

if __name__ == "__main__":
    my_func()
