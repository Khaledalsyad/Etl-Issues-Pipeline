def logger_decorator(func):
    def inner(*args, **kwargs):
        print(f'starts execution of {func.__name__}')

        result = func(*args, **kwargs)

        print(f'end execution of {func.__name__}')

        return result

    return inner