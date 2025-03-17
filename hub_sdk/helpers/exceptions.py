# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from hub_sdk.config import HUB_EXCEPTIONS


def suppress_exceptions() -> None:
    """
    Suppress exceptions locally based on the global HUB_EXCEPTIONS flag.

    If the HUB_EXCEPTIONS flag is set to False, this function raises the caught exception,
    allowing it to propagate and be handled elsewhere. If the flag is set to True,
    the function suppresses the exception, effectively handling it locally.

    Examples:
        # Set the HUB_EXCEPTIONS constant to control exception handling globally
        >>> HUB_EXCEPTIONS = False

        >>> try:
        ...     # Your code that may raise an exception
        ...     pass
        ... except ValueError as e:
        ...     # The exception will be suppressed if HUB_EXCEPTIONS is True
        ...     suppress_exceptions()
        ...     # Exception handling continues here if HUB_EXCEPTIONS is False

    Notes:
        This function is designed to be used in conjunction with the global HUB_EXCEPTIONS constant
        to control exception handling behavior across multiple parts of the codebase.
    """
    if not HUB_EXCEPTIONS:
        raise
