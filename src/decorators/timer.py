import time

def timer(Func):

    def inner(*args, **kwargs):

        start = time.time()
        
        result = Func(*args, **kwargs)

        end= time.time()

        print(F"The Function {Func.__name__} take {end - start:.2F} Secound")
        
        return result

    return inner