# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import threading


def threaded(func):
    """
    Multi-threads a target function and returns thread.

    Usage: @threaded decorator.
    """

    def wrapper(*args, **kwargs):
        """Multi-threads a given function and returns the thread."""
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread

    return wrapper
