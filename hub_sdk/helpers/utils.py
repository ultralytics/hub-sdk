# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

import threading


def threaded(func):
    """
    Multi-threads a target function and returns the thread.

    Args:
        func (function): The function to be executed in a separate thread.

    Returns:
        (threading.Thread): The thread in which the function is executed.

    Example:
        ```python
        @threaded
        def example_function(data):
            print(data)

        thread = example_function('Hello, world!')
        ```
    """

    def wrapper(*args, **kwargs):
        """Multi-threads a given function and returns the thread."""
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper
