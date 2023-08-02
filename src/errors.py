class InvalidParameterError(ValueError):
    """Raised when one of the one or more of the action parameters are missing."""

class ConfluenceApiError(ValueError):
    """Raised when the Confluence API functions return invalid data."""

class SubstringNotFoundError(LookupError):
    """Raised when a required substring is not found in a text."""