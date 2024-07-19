# Ultralytics HUB-SDK 🚀, AGPL-3.0 License

from hub_sdk.config import HUB_EXCEPTIONS


def suppress_exceptions() -> None:
    """
    Suppress exceptions based on the global HUB_EXCEPTIONS flag.

    If the HUB_EXCEPTIONS flag is set to False, this function raises the caught exception, allowing it to propagate and
    be handled elsewhere. If the flag is set to True, the function suppresses the exception, effectively handling it
    locally.

    Returns:
        (None)

    Example:
        ```python
        HUB_EXCEPTIONS = False

        try:
            # Your code that may raise an exception
        except ValueError as e:
            # The exception will be suppressed if HUB_EXCEPTIONS is True
            suppress_exceptions()
            # Exception handling continues here if HUB_EXCEPTIONS is False
        ```

    Note:
        This function is designed to be used in conjunction with the global HUB_EXCEPTIONS constant to control exception
        handling behavior across multiple parts of the codebase.
    """
    if not HUB_EXCEPTIONS:
        raise
