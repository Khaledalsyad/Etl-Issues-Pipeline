def Retry(retries= 3):

    def decorator(Func):

        def inner(*args, **kwargs):

            for attempt in range(retries):
                try:
                    return Func(*args, **kwargs)
                except Exception as e:
                    print(f"The Retry {attempt + 1} and excecution {e}")

        return inner

    return decorator 
            