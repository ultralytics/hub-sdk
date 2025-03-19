# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import threading


def threaded(func):
    """
    Multi-threads a target function by default and returns the thread or function result.

    This decorator provides flexible execution of the target function, either in a separate thread or synchronously.
    By default, the function runs in a thread, but this can be controlled via the 'threaded=False' keyword argument
    which is removed from kwargs before calling the function.

    Args:
        func (callable): The function to be potentially executed in a separate thread.

    Returns:
        (callable): A wrapper function that either returns a daemon thread or the direct function result.

    Example:
        >>> @threaded
        ... def process_data(data):
        ...     return data
        >>>
        >>> thread = process_data(my_data)  # Runs in background thread
        >>> result = process_data(my_data, threaded=False)  # Runs synchronously, returns function result
    """

    def wrapper(*args, **kwargs):
        """
        Multi-threads a given function based on 'threaded' kwarg and returns the thread or function result.

        Args:
            *args: Variable length argument list to pass to the target function.
            **kwargs: Arbitrary keyword arguments to pass to the target function.

        Keyword Args:
            threaded (bool, optional): Whether to run in a thread. Defaults to True.

        Returns:
            Union[threading.Thread, Any]: Either a started daemon thread or the direct result of the function call,
                depending on the value of the 'threaded' parameter.
        """
        if kwargs.pop("threaded", True):  # run in thread
            thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
            thread.start()
            return thread
        else:
            return func(*args, **kwargs)

    return wrapper
